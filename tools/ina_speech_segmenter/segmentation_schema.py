class SegmentationSchema:
  def addSegment(self, label, gender, start, end):
    print('adding segment')
    self.segments.append(SegmentationSchemaSegment(label, gender, start, end))
    print(self.segments)
    return
  def __init__(self, filename):
    self.media = SegmentationSchemaMedia(filename)
    self.segments = []


class SegmentationSchemaMedia:
  filename = ""
  def __init__(self, filename):
    self.filename = filename

class SegmentationSchemaSegment:
  label = ""
  start = 0
  end = 0
  def __init__(self, label, gender, start, end):
    self.label = label
    if len(gender) > 0:
      self.gender = gender
    self.start = start
    self.end = end