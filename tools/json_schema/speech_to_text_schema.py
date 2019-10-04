class SpeechToText:
	def __init__(self, media=None, result=None):
		if media is None:
			self.media = SpeechToTextMedia()
		else:
			 self.media = media
		if result is None:
			self.result = SpeechToTextResult()
		else:
			 self.result = media

class SpeechToTextMedia:
	filename = ""
	duration = 0
	def __init__(self, duration = 0, filename = ""):
		self.duration = duration
		self.filename = filename

class SpeechToTextResult:
	transcript = ""
	words = []
	def __init__(self, words=[], transcript=""):
		self.transcript = transcript
		self.words = words
	def addWord(self, type, start, end, text, scoreType, scoreValue):
		newWord = SpeechToTextWord(type, start, end, text, scoreType, scoreValue)
		self.words.extend(newWord)

class SpeechToTextWord:
	type = ""
	start = 0.00
	end = 0.00
	text = ""
	score = None
	def __init__(self, type, start, end, text, scoreType, scoreValue):
		self.score = SpeechToTextScore(scoreType, scoreValue)
		self.type = type
		self.start = start
		self.end = end
		self.text = text


class SpeechToTextScore:
	type = ""
	scoreValue = 0.0
	def __init__(self, scoreType, scoreValue):
		self.type = scoreType
		self.scoreValue = scoreValue


	