#!/usr/bin/env python3

import json
import os
import sys

from ..json_schema.segmentation_schema import SegmentationSchema

from speech_to_text_schema import SpeechToText, SpeechToTextMedia, SpeechToTextResult, SpeechToTextScore, SpeechToTextWord

def main():

	(stt_json, adj_json, output_json) = sys.argv[1:4]
    #test
    print(stt_json)
    print(adj_json)
    print(output_json)
	

if __name__ == "__main__":
	main()