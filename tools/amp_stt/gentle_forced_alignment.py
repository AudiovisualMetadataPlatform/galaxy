#!/usr/bin/env python3

import json
import os
import os.path
import shutil
import subprocess
import sys
import tempfile

import uuid


def main():
	(input_audio_file, input_transcript_file, json_file) = sys.argv[1:4]
	try:
		# Create random temp names
		tmpAudioName = str(uuid.uuid4())
		tmpTranscriptName = str(uuid.uuid4())

		# Define directory accessible to singularity container
		tmpdir = '/Users/dan'

		# Create temp file paths
		temp_audio_file = f"{tmpdir}/{tmpAudioName}.dat"
		temp_transcript_file = f"{tmpdir}/{tmpTranscriptName}.dat"
		temp_output_file = f"{tmpdir}/{tmpAudioName}.json"

		# Load the original transcript as input into gentle
		with open(input_transcript_file, "r") as input_ts_file:
			orig_transcript = json.load(input_ts_file)

			# Write the transcript to an input file into gentle
			with open(temp_transcript_file, "w") as text_file:
				text_file.write(orig_transcript["results"]["transcript"])

			# Copy the audio file to a location accessible to the singularity container
			shutil.copy(input_audio_file, temp_audio_file)

			# Run gentle
			print("Running gentle")
			r = subprocess.run(["singularity", "run", "/Users/dan/documents/IU/gentle-singularity.sif", temp_audio_file, temp_transcript_file, "-o", temp_output_file], stdout=subprocess.PIPE)
			print("Finished running gentle")

			print("Creating amp transcript output")
			write_amp_json(temp_output_file, orig_transcript, json_file)
	except Exception as e:
		print(e)

	if os.path.exists(temp_audio_file):
	 	os.remove(temp_audio_file)

	if os.path.exists(temp_transcript_file):
		os.remove(temp_transcript_file)

	if os.path.exists(temp_output_file):
		os.remove(temp_output_file)
	
	exit(r.returncode)

def write_amp_json(temp_gentle_output, original_transcript, amp_transcript_output):
	# Create the amp transcript
	output = dict()
	with open(temp_gentle_output, "r") as gentle_output_file:
		gentle_output = json.load(gentle_output_file)
		output["media"] = original_transcript["media"]
		output["results"] = dict()
		output["results"]["transcript"] = original_transcript["results"]["transcript"]
		output["results"]["words"] = list()
		for word in gentle_output["words"]:
			# Make sure we have all the data
			if word["case"] == 'success':
				output["results"]["words"].append(
					{
						"type": "pronunciation", 
						"start": word["start"], 
						"end": word["end"], 
						"text": word["word"],
						"score": {
								"type": "confidence", 
								"scoreValue": 1.0
						} 
					}
				)
		with open(amp_transcript_output, 'w') as outfile:
			json.dump(output, outfile)
if __name__ == "__main__":
	main()
