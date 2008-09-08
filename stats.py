#
# Copyright 2008 Ralph M. Churchill
#

class Stats(object):
	def __init__(self):
		self.__correct = self.__incorrect = self.__questions = 0

	def right(self):
		self.correct += 1
		self.questions += 1

	def wrong(self):
		self.incorrect += 1

	def to_hash(self):
		return {'correct':self.correct,
				'incorrect':self.incorrect,
				'questions':self.questions,
				'answered':self.answered(),
				}

	def get_correct(self): return self.__correct
	def set_correct(self,c): self.__correct = c
	def get_incorrect(self): return self.__incorrect
	def set_incorrect(self,c): self.__incorrect = c
	def get_questions(self): return self.__questions
	def set_questions(self,q): self.__questions = q
	def answered(self):
		return "%d %s" % (self.__questions, "question" if self.__questions == 1 else "questions")
	
	correct = property(get_correct,set_correct)
	incorrect = property(get_incorrect,set_incorrect)
	questions = property(get_questions,set_questions)

