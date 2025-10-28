import json
import logging

from galaxy.datatypes.data import get_file_peek, Text
from galaxy.datatypes.text import Json
from galaxy.datatypes.sniff import build_sniff_from_prefix, FilePrefix
from galaxy.datatypes.protocols import DatasetProtocol
from galaxy.util import nice_size

log = logging.getLogger(__name__)


###########################
## AMP extended Json Types
###########################

@build_sniff_from_prefix
class AmpJson(Json):
    label = "AMP JSON"

    def set_peek(self, dataset: DatasetProtocol, **kwd) -> None:
        super().set_peek(dataset);
        if not dataset.dataset.purged:
            dataset.blurb = self.label

    def display_peek(self, dataset: DatasetProtocol) -> str:
        try:
            return dataset.peek
        except Exception:
            return f"{self.label} file ({nice_size(dataset.get_size())})"

@build_sniff_from_prefix
class Segment(AmpJson):
    file_ext = "segment"
    label = "AMP Segment JSON"

    def _looks_like_json(self, file_prefix: FilePrefix) -> bool:
        # Pattern used by SequenceSplitLocations
        if file_prefix.file_size < 50000 and not file_prefix.truncated:
            # If the file is small enough - don't guess just check.
            try:
                # exclude simple types, must set format in these cases
                item = json.loads(file_prefix.contents_header)
                assert isinstance(item, (list, dict))
                # must contain media and segments
                return 'media' in item and 'segments' in item
            except Exception:
                return False
        else:
            # must start with JSON prefix and contain media + segments
            start = file_prefix.string_io().read(500).strip()
            if start and (start.startswith("[") or start.startswith("{")):
                return "\"media\":" in start and "\"segments\":" in start
            return False
       
@build_sniff_from_prefix
class Transcript(AmpJson):
    file_ext = "transcript"
    label = "AMP Transcript JSON"

    def _looks_like_json(self, file_prefix: FilePrefix) -> bool:
        # Pattern used by SequenceSplitLocations
        if file_prefix.file_size < 50000 and not file_prefix.truncated:
            # If the file is small enough - don't guess just check.
            try:
                # exclude simple types, must set format in these cases
                item = json.loads(file_prefix.contents_header)
                assert isinstance(item, (list, dict))
                # must contain media and results.transcript
                if not ('media' in item and 'results' in item):
                    return False                
                results = item['results']
                return 'transcript' in results
            except Exception:
                return False
        else:
            # must start with JSON prefix and contain media + results + transcript
            start = file_prefix.string_io().read(500).strip()
            if start and (start.startswith("[") or start.startswith("{")):
                return "\"media\":" in start and "\"results\":" in start and "\"transcript\":" in start 
            return False
       
@build_sniff_from_prefix
class Ner(AmpJson):
    file_ext = "ner"
    label = "AMP NER JSON"
    
    def _looks_like_json(self, file_prefix: FilePrefix) -> bool:
        # Pattern used by SequenceSplitLocations
        if file_prefix.file_size < 50000 and not file_prefix.truncated:
            # If the file is small enough - don't guess just check.
            try:
                # exclude simple types, must set format in these cases
                item = json.loads(file_prefix.contents_header)
                assert isinstance(item, (list, dict))
                # must contain media and entities
                return 'media' in item and 'entities' in item
            except Exception:
                return False
        else:
            # must starts with JSON prefix and contain media + entities
            start = file_prefix.string_io().read(500).strip()
            if start and (start.startswith("[") or start.startswith("{")):
                return "\"media\":" in start and "\"entities\":" in start
            return False
 
@build_sniff_from_prefix
class Shot(AmpJson):
    file_ext = "shot"
    label = "AMP Shot JSON"

    def _looks_like_json(self, file_prefix: FilePrefix) -> bool:
        # Pattern used by SequenceSplitLocations
        if file_prefix.file_size < 50000 and not file_prefix.truncated:
            # If the file is small enough - don't guess just check.
            try:
                # exclude simple types, must set format in these cases
                item = json.loads(file_prefix.contents_header)
                assert isinstance(item, (list, dict))
                # must contain media and shots
                return 'media' in item and 'shots' in item
            except Exception:
                return False
        else:
            # must start with JSON prefix and contain media + shots
            start = file_prefix.string_io().read(500).strip()
            if start and (start.startswith("[") or start.startswith("{")):
                return "\"media\":" in start and "\"shots\":" in start
            return False
           
@build_sniff_from_prefix
class VideoOcr(AmpJson):
    file_ext = "vocr"
    label = "AMP Video OCR JSON"

    def _looks_like_json(self, file_prefix: FilePrefix) -> bool:
        # Pattern used by SequenceSplitLocations
        if file_prefix.file_size < 50000 and not file_prefix.truncated:
            # If the file is small enough - don't guess just check.
            try:
                # exclude simple types, must set format in these cases
                item = json.loads(file_prefix.contents_header)
                assert isinstance(item, (list, dict))
                # must contain media + frames
                if not ('media' in item and 'frames' in item):
                    return False                
                # must contain frames[0].objects[0].text
                frames = item['frames']
                if len(frames) > 0 and 'objects' in frames[0]:
                    objects = frames[0]['objects']
                    return len(objects) > 0 and 'text' in objects[0]
                else:
                    return False
            except Exception:
                return False
        else:
            # must start with JSON prefix and contain media + frames + objects + text
            start = file_prefix.string_io().read(500).strip()
            if start and (start.startswith("[") or start.startswith("{")):
                return "\"media\":" in start and "\"frames\":" in start and "\"objects\":" in start and "\"text\":" in start
            return False    

# Note that the schema for VideoOcr and Face are very similar, except that the former contains "text" while the latter contains "name"
# If there is no frame or no objects in a frame then we can't tell the two types apart, and the sniffer may fall back to JSON.
   
@build_sniff_from_prefix
class Face(AmpJson):
    file_ext = "face"
    label = "AMP Face JSON"

    def _looks_like_json(self, file_prefix: FilePrefix) -> bool:
        # Pattern used by SequenceSplitLocations
        if file_prefix.file_size < 50000 and not file_prefix.truncated:
            # If the file is small enough - don't guess just check.
            try:
                # exclude simple types, must set format in these cases
                item = json.loads(file_prefix.contents_header)
                assert isinstance(item, (list, dict))
                # must contain media and frames
                if not ('media' in item and 'frames' in item):
                    return False                
                # must contain frames[0].objects[0].name
                frames = item['frames']
                if len(frames) > 0 and 'objects' in frames[0]:
                    objects = frames[0]['objects']
                    return len(objects) > 0 and 'name' in objects[0]
                else:
                    return False
            except Exception:
                return False
        else:
            # must start with JSON prefix and contain media + frames + objects + name
            start = file_prefix.string_io().read(500).strip()
            if start and (start.startswith("[") or start.startswith("{")):
                return "\"media\":" in start and "\"frames\":" in start and "\"objects\":" in start and "\"name\":" in start
            return False
           
@build_sniff_from_prefix
class Vtt(Text):
    file_ext = "vtt"
    label = "Web VTT"

    # inherit super (Text) set_peek, no need to overwrite
    
    def get_mime(self) -> str:
        """Returns the mime type of the datatype"""
        return 'text/vtt'

    def sniff_prefix(self, file_prefix: FilePrefix) -> bool:
        # WEBVTT is the header of a WebVTT file. 
        # We assume that no other kind of text files use this as the first line content; otherwise further checking  
        # on following lines can be done to detect if they match the regexp patterns for timestamp & speaker diarization.
        try:
            first_line = file_prefix.string_io().readline().strip()      
            log.debug ("Vtt.sniff_prefix: first_line = " + first_line)  
            if (first_line == "WEBVTT"):
                log.debug ("Vtt.sniff_prefix: return true")  
                return True
            else:
                log.debug ("Vtt.sniff_prefix: return false")  
                return False
        except Exception as e:
            log.exception(e)
            return False              

    def set_peek(self, dataset: DatasetProtocol, **kwd) -> None:
        super().set_peek(dataset);
        if not dataset.dataset.purged:
            dataset.blurb = self.label

    def display_peek(self, dataset: DatasetProtocol) -> str:
        try:
            return dataset.peek
        except Exception:
            return f"{self.label} file ({nice_size(dataset.get_size())})"
        

