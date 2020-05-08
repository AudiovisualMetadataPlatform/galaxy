#!/usr/bin/env python3

import json
import sys
import os


# Convert IIIF manifest JSON file to standard NER output JSON file.
# Usage: iiif_to_ner.py output_iiif input_ner output_ner
def main():
    # parse command line arguments
    output_iiif = sys.argv[1]    # input file generated by NER in standard AMP json format to convert from
    input_ner = sys.argv[2]        # input file to feed to NER editor in IIIF json format to convert to
    output_ner = sys.argv[3]    # context info as json string needed for creating HMGM tasks

    # parse output IIIF and original input NER
    with open(output_iiif, 'r') as iiif_file:
        iiif_data = json.load(iiif_file)
    with open(input_ner, 'r') as ner_file:
        ner_data = json.load(ner_file)

    # update entities in original input NER
    entity_dict = build_ner_entity_dictionary(ner_data)
    ner_data["entities"] = generate_ner_entities(iiif_data, entity_dict)

    # write entities back to output NER
    with open(output_ner, "w") as outfile: 
        json.dump(ner_data, outfile) 


# Build a dictionary for NER entities with start time as key and entity as value, to allow efficient searching of entity by timestamp.
# Note: Matching IIIF annoation with NER entity by timestamp is based on the assumption that timestamp can not be changed by NER editor,
# (it can be added/deleted), and at any given time there can be only one entity; thus timestamp can uniquely identify an entity in both IIIF and NER.
def build_ner_entity_dictionary(ner_data):
    entity_dict = {}

    # create a {start, entity} tuple for each entity in ner_data 
    for entity in ner_data["entities"]:
        entity_dict[entity["start"]] = entity

    return entity_dict


# Generate NER entities using the given iiif_data and entity_dict
def generate_ner_entities(iiif_data, entity_dict):
    entities = []

    # update/create an NER entity for each IIIF annotation in iiif_data;
    for annotation in iiif_data["annotations"][0]["items"]:        
        time = annotation["target"]["selector"]["t"]
        if time in entity_dict:
            # if the annotation timestamp matches an entity start time, update the entity text/type with that from the annotation
            entity = entity_dict[time]
            entity["type"] = annotation["body"]["value"]
            entity["text"] = annotation["label"]["en"][0]
            # start, score and other fields in entity remain the same
        else:
            # otherwise create a new entity using fields in the annotation and with a full score    
            entity = {
                "type": annotation["body"]["value"],
                "text": annotation["label"]["en"][0],
                "start": time,
                "score": {
                    "type": "relevance",
                    "scoreValue": 1.0
                }
            }
        entities.append(entity)

    # those in original NER but not in IIIF (i.e. deleted by NER editor) are excluded from the entity list
    return entities


if __name__ == "__main__":
    main()    
