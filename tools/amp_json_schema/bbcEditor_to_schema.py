#!/usr/bin/env python3

import json
import sys
import os
import aws_transcribe_to_schema
from speech_to_text_schema import SpeechToText, SpeechToTextMedia, SpeechToTextResult, SpeechToTextScore, SpeechToTextWord

# Convert editor output to standardized json
def main():
    #(editor_output_file, output_json_file, media_file) = sys.argv[1:4]
    output_json_file = 'tools/amp_json_schema/output.json'
    editor_output_file = 'tools/amp_json_schema/Galaxy70-[HMGM_Transcript_Correction_on_data_26].json'
    media_file = 'myfile.mp3'
    
    with open(editor_output_file) as json_file:
        d = json.load(json_file)
        data = eval(json.dumps(d))
	
    result = SpeechToTextResult()

    transcript = word_type = text = ''
    confidence = start_time = end_time = -1
    duration = 0.0

    #Standardising draft js format
    if "entityMap" in data.keys():
        entityMap = data["entityMap"]
        for entity in entityMap.values():
            punctuation = ''
            if "data" in entity:
                if "text" in entity["data"].keys():
                    text = entity["data"]["text"]
                    transcript += text+" "
                    if text[-1] in [',','.','!','?']:
                        punctuation = text[-1]
                        text = text[0:-1]

                if "type" in entity:
                    entity_type = entity["type"]
                    if entity_type == "WORD":
                        word_type = "pronunciation"
                        if "start" in entity["data"]:
                            start_time = float(entity["data"]["start"])

                        if "end" in entity["data"]:
                            end_time = float(entity["data"]["end"])

                        if end_time > duration:
                            duration = end_time
                    else:
                        word_type = entity_type
                
                if "confidence" in entity["data"].keys():
                    confidence = float(entity["data"]["confidence"])
            result.addWord(word_type, start_time, end_time, text, "confidence",confidence)   
            if len(punctuation) > 0:
                result.addWord('punctuation', None, None, punctuation, "confidence",confidence)

        result.transcript = transcript 

    #Standardizing AWS Transcribe file
    elif "jobName" in data.keys() and "results" in data.keys():
        transcripts = data["results"]["transcripts"]
        for t in transcripts:
            result.transcript = result.transcript + t["transcript"]
        
        # Parse items (words)
        items = data["results"]["items"]
	
        # For each item, get the necessary parts and store as a word
        for i in items:
            alternatives = i["alternatives"]
            # Choose an alternative
            max_confidence = 0.00
            text = ""

            # Each word is stored as an "alternative".  Get the one with the maximum confidence
            for a in alternatives:
                if float(a["confidence"]) >= max_confidence:
                    max_confidence = float(a["confidence"])
                    text = a["content"]

            end_time = -1
            start_time = -1

            # Two types (punctionation, pronunciation).  Only keep times for pronunciation
            if i["type"] == "pronunciation":
                end_time = float(i["end_time"])
                start_time = float(i["start_time"])

                # If this is the greatest end time, store it as duration
                if end_time > duration:
                    duration = end_time
            # Add the word to the result
            result.addWord(i["type"], start_time, end_time, text, "confidence", max_confidence)

    #Output the file as it is
    else:
        # Write the output
        outputFile = editor_output_file

    # Create the media object
    media = SpeechToTextMedia(duration, media_file)

    # Create the final object
    outputFile = SpeechToText(media, result)

    # Write the output
    write_output_json(outputFile, output_json_file)


# Serialize schema obj and write it to output file
def write_output_json(input_json, json_file):
	with open(json_file, 'w') as outfile:
		json.dump(input_json, outfile, default=lambda x: x.__dict__)

if __name__ == "__main__":
	main()