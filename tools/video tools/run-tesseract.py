# Python imports

import pytesseract
import os
import json
import sys
import time
import subprocess

from datetime import timedelta
from decimal import Decimal

#clear old images
#!rm -rf "temp"/*


def main():
	(input_file, start, duration) = sys.argv[1:4]
	os.mkdir("temp/"+input_file[:-4])
	command = "ffmpeg -i "+input_file+ " -an -vf fps=2 'temp/"+input_file+"/frame_%05d.jpg'"
	#print(command)
	subprocess.call(command, shell=True)
	#command = "rm -R temp/"
	#subprocess.call(command)  	
	
	#Tesseract part starts here	
	script_start = time.time()
	directory = "temp/" + input_file
	output_name =  input_file+ "-ocr.json"
	
	# Get some stats on the video
	dim = getDimensions(input_file)
	framerate = getFramerate(input_file)
	numFrames = getNumFrames(input_file)

	output = {"media": {"filename": s["filename"],
			"duration": str(s["sample_duration"]),
          		"framerate": framerate,
          		"numFrames": numFrames,
          		"resolution": {
              			"width": int(dim[0]),
              			"height": int(dim[1])
          			}
          
			},
		"frames": []
		}
	#for every saved frame
	for num, img in enumerate(sorted(os.listdir(directory))): 
		start_time =+ (.5*num) 
		frameList = {"start": str(start_time),
			"boundingBoxes": []
			}
      
		#Run OCR
		result = pytesseract.image_to_data(Image.open(directory+"/"+img), output_type=Output.DICT)
		
		#For every result, make a box & add it to the list of boxes for this framecalled frameList
		for i in range(len(result["text"])): 
			if result["text"][i].strip(): #if the text isn't empty/whitespace
				box = {
					"text": result["text"][i],
					"score": {
						"type":"confidence",
						"scoreValue": result["conf"][i]
				      		},
				      	# relative coords
				      	"vertices": {
						"xmin": result["left"][i]/output["media"]["resolution"]["width"],
						"ymin": result["top"][i]/output["media"]["resolution"]["height"],
						"xmax": (result["left"][i] + result["width"][i])/output["media"]["resolution"]["width"],
						"ymax": (result["top"][i] + result["height"][i])/output["media"]["resolution"]["height"]
						}
				 	}
				frameList["boundingBoxes"].append(box)
      
      		#save frame if it had text
		if len(frameList["boundingBoxes"]) > 0:
			output["frames"].append(frameList)
			#print(frame)
  
	with open(output_name, 'w') as outfile:
		json.dump(output, outfile)
  	
	print("Finished " + output_name + " in " + str(time.time()-script_start) + "s")		

	#os.remove("temp/"+input_file+"_*.jpg")


def call_tesseract():
	script_start = time.time()
	output_name =  input_file+ "-ocr.json"
	

# UTIL FUNCTIONS
def getDimensions(path):
	dim_cmd = "ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "+path
	print("========The dim_cmd is:",dim_cmd)
	dim = subprocess.call(dim_cmd, shell=True)
	print(path)
	print("dim======>",dim)
	return dim[0].split("x")


def getFramerate(path):
	fr_cmd = "ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=nokey=1:noprint_wrappers=1 "+path
	fr = subprocess.call(fr_cmd, shell=True)	
	print("fr=======>",int(fr[0].split('/')[0]))
	return int(fr[0].split('/')[0])

def getNumFrames(path):
	nf_cmd = "ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1 "+path
	nf = subprocess.call(nf_cmd, shell=True)	
	print("nf======>",int(nf[0]))
	return int(nf[0])
  


if __name__ == "__main__":
	main()
