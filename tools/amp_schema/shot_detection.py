from collections import namedtuple
import json

class ShotDetectionSchema:
    def __init__(self, media=None, shots = []):
        self.shots = []
        if media is None:
            self.media = ShotDetectionMediaSchema()
        else:
             self.media = media
             

class ShotDetectionMediaSchema:
    filename = ""
    duration = 0

    def __init__(self, filename = "", duration = 0):
        self.duration = duration
        self.filename = filename

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)

class ShotDetectionShotSchema:
    type = ""
    start = 0
    end = 0
    
    def __init__(self, type = None, start = None, end = None):
        self.type = type
        self.start = start
        self.end = end

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(**json_data)


