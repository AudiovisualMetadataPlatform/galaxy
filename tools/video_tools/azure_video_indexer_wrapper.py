#!/usr/bin/env python3
import sys
import requests
import logging
import time
import json
import tempfile
import os
from datetime import timedelta
from datetime import datetime
import math

from requests_toolbelt import MultipartEncoder

sys.path.insert(0, os.path.abspath('../../../../../tools/amp_json_schema'))

from video_ocr import VideoOcrSchema, VideoOcrMediaSchema, VideoOcrResolutionSchema, VideoOcrFrameSchema, VideoOcrBoundingBoxSchema, VideoOcrBoundingBoxScoreSchema, VideoOcrBoundingBoxVerticesSchema

def main():
	apiUrl = "https://api.videoindexer.ai"

	(input_file, accountId, apiKey, location, output_from_azure_simple, output_from_azure, output_amp_ocr_schema) = sys.argv[1:8]

	try:
		import http.client as http_client
	except ImportError:
		# Python 2
		import httplib as http_client

	# You must initialize logging, otherwise you'll not see debug output.
	logging.basicConfig()

	# Turn on HTTP debugging here
	http_client.HTTPConnection.debuglevel = 1

	# Get an authorization token for subsequent requests
	auth_token = get_auth_token(apiUrl, location, accountId, apiKey)
	
	# Upload the video and get the ID to reference for indexing status and results
	videoId = upload_video(apiUrl, location, accountId, auth_token, input_file)

	# Get the auth token associated with this video	
	video_auth_token = get_video_auth_token(apiUrl, location, accountId, apiKey, videoId)

	# Check on the indexing status
	while True:
		state = get_processing_status(apiUrl, location, accountId, videoId, video_auth_token)
		
		# We have a status other than uploaded or processing, it is complete
		if state != "Uploaded" and state != "Processing":
			break
		# Wait a bit before checking again
		time.sleep(30)

	# Turn on HTTP debugging here
	http_client.HTTPConnection.debuglevel = 1

	# Get the video index json (simple)
	simple_json = get_video_index_json(apiUrl, location, accountId, videoId, auth_token, apiKey)
	write_json_file(simple_json, output_from_azure_simple)

	# Get the advanced OCR via a URL 
	artifacts_url = get_artifacts_url(apiUrl, location, accountId, videoId, auth_token)
	advanced_json = get_artifacts(artifacts_url, output_from_azure)

	# Parse the json
	parse_json(input_file, output_amp_ocr_schema, advanced_json, simple_json)
	

# Convert the timestamp to total seconds
def convertTimestampToSeconds(timestamp):
	try:
		x = datetime.strptime(timestamp, '%H:%M:%S.%f')
	except ValueError:
		x = datetime.strptime(timestamp, '%H:%M:%S')
	hourSec = x.hour * 60.0 * 60.0
	minSec = x.minute * 60.0
	total_seconds = hourSec + minSec + x.second + x.microsecond/600000

	return total_seconds

# Calculate the frame index based on the start time and frames per second
def getFrameIndex(start_time, fps):
	startSeconds = convertTimestampToSeconds(start_time)
	frameSeconds = 1/fps
	frameFraction = startSeconds/frameSeconds
	frame = 0.0
	ceilFrame = abs(math.ceil(frameFraction) - frameFraction)
	floorFrame = abs(math.floor(frameFraction) - frameFraction)
	if ceilFrame < floorFrame:
		frame = math.ceil(frameFraction)
	else:
		frame = math.floor(frameFraction)

	return frame

# Parse the results
def parse_json(input_file, output_file, advanced_json, simple_json):
	amp_ocr = VideoOcrSchema()

	# Create the resolution obj
	width = advanced_json["width"]
	height = advanced_json["height"]
	resolution = VideoOcrResolutionSchema(width, height)

	# Create the media object
	framerate = advanced_json["framerate"]
	duration = simple_json["summarizedInsights"]["duration"]["seconds"]
	frames = int(framerate * duration)
	amp_media  = VideoOcrMediaSchema(duration, input_file, framerate, frames, resolution)
	amp_ocr.media = amp_media

	# Create a dictionary of all the frames [FrameNum : List of Terms]
	frame_dict = createFrameDictionary(simple_json['videos'], framerate)
	
	# Convert to amp frame objects with bounding boxes
	amp_frames = createAmpFrames(frame_dict, framerate)
	
	# Add the frames to the schema
	amp_ocr.frames = amp_frames

	# Write the output json file
	write_json_file(amp_ocr, output_file)

# Create a list of terms for each of the frames
def createFrameDictionary(video_json, framerate):
	frame_dict={}
	for v in video_json:
		for ocr in v['insights']['ocr']:
			for i in ocr['instances']:
				# Get where this term starts and end in terms of frame number
				frameIndexStart = getFrameIndex(i['start'], framerate)
				frameIndexEnd = getFrameIndex(i['end'], framerate)
				# Create a temp obj to store the results
				newOcr = {
					"text" : ocr["text"],
					"language" : ocr["language"],
					"confidence" : ocr["confidence"],
					"left" : ocr["left"],
					"top" : ocr["top"],
					"width" : ocr["width"],
					"height" : ocr["height"]
				}
				# From the first frame to the last, add the bounding box info
				for frameIndex in range(frameIndexStart, frameIndexEnd + 1):
					# If it already exists, append it.  Otherwise create new list
					if frameIndex in frame_dict.keys():
						thisFrame = frame_dict[frameIndex]
						thisFrame.append(newOcr)
						frame_dict[frameIndex] = thisFrame
					else:
						frame_dict[frameIndex] = [newOcr]
	return frame_dict

# Convert the dictionary into AMP objects we need
def createAmpFrames(frame_dict, framerate):
	amp_frames = []
	for frameNum, boundingBoxList in frame_dict.items():
		bounding_boxes = []
		for b in boundingBoxList:
			amp_score = VideoOcrBoundingBoxScoreSchema("confidence", b["confidence"])
			bottom = b['top'] - b['height']
			right = b['left'] + b['width']
			amp_vertice = VideoOcrBoundingBoxVerticesSchema(b['left'], bottom, right, b['top'])
			amp_bounding_box = VideoOcrBoundingBoxSchema(b["text"], b["language"], amp_score, amp_vertice)
			bounding_boxes.append(amp_bounding_box)
		amp_frame = VideoOcrFrameSchema((frameNum) * (1/framerate), bounding_boxes)
		amp_frames.append(amp_frame)
	
	amp_frames.sort(key=lambda x: x.start, reverse = False)
	return amp_frames

# Retrieve the "artifacts" (ocr json) from the specified url
def get_artifacts(artifacts_url, output_name):
	r = requests.get(url = artifacts_url)
	with open(output_name, 'wb') as f:
		f.write(r.content)
	return json.loads(r.content)

# Get the url where the artifacts json is stored
def get_artifacts_url(apiUrl, location, accountId, videoId, auth_token):
	url = apiUrl + "/" + location + "/Accounts/" + accountId + "/Videos/" + videoId + "/ArtifactUrl"
	params = {'accessToken':auth_token,
				'type':'ocr'}
	r = requests.get(url = url, params = params)
	return r.text.replace("\"", "")

# Get the video index json, which contains OCR data
def get_video_index_json(apiUrl, location, accountId, videoId, auth_token, apiKey):
	url = apiUrl + "/" + location + "/Accounts/" + accountId + "/Videos/" + videoId + "/Index"
	params = {'accessToken':auth_token }
	headers = {"Ocp-Apim-Subscription-Key": apiKey}
	r = requests.get(url = url, params=params, headers = headers) 
	return json.loads(r.text)

# Get the processing status of the video
def get_processing_status(apiUrl, location, accountId, videoId, video_auth_token):
	video_url = apiUrl + "/" + location + "/Accounts/" + accountId + "/Videos/" + videoId + "/Index"
	params = {'accessToken':video_auth_token,
				'language':'English'}
	r = requests.get(url = video_url, params = params)
	data = json.loads(r.text)
	if 'videos' in data.keys():
		videos = data['videos']
		if 'state' in videos[0].keys():
			return videos[0]['state']
	return "Error"

# Create the auth token request
def request_auth_token(url, apiKey):
	params = {'allowEdit':True} 
	headers = {"Ocp-Apim-Subscription-Key": apiKey}
	# sending get request and saving the response as response object 
	r = requests.get(url = url, params = params, headers=headers) 
	if r.status_code == 200:
		return r.text.replace("\"", "")
	else:
		print("Auth failure")
		print(r)
		exit(1)

# Get general auth token
def get_auth_token(apiUrl, location, accountId, apiKey):
	token_url = apiUrl + "/auth/" + location + "/Accounts/" + accountId + "/AccessToken"
	return request_auth_token(token_url, apiKey)

# Get video auth token
def get_video_auth_token(apiUrl, location, accountId, apiKey, videoId):
	token_url = apiUrl + "/auth/" + location + "/Accounts/" + accountId + "/Videos/" + videoId + "/AccessToken"
	return request_auth_token(token_url, apiKey)

# Upload the video using multipart form upload
def upload_video(apiUrl, location, accountId, auth_token, input_file):

	# Create a unique file name 
	millis = int(round(time.time() * 1000))

	upload_url = apiUrl + "/" + location +  "/Accounts/" + accountId + "/Videos"
	
	data = {}
	with open(input_file, 'rb') as f:
		data["file"] = ("file", f)
		m = MultipartEncoder(fields=data)
		headers = {'Content-Type':  m.content_type}
		params = {'accessToken':auth_token,
				'name':'amp_video_' + str(millis),
				'description':'AMP File Upload',
				'privacy':'private',
				'partition':'No Partition'}
		r = requests.post(upload_url, data=m, headers=headers, params = params)
		
		if r.status_code != 200:
			print("Upload failure")
			print(r)
			exit(1)
		else:
			data = json.loads(r.text)
			if 'id' in data.keys():
				return data['id']
			else:
				exit(1)

# Serialize obj and write it to output file
def write_json_file(obj, output_file):
    # Serialize the object
    with open(output_file, 'w') as outfile:
        json.dump(obj, outfile, default=lambda x: x.__dict__)

if __name__ == "__main__":
	main()
