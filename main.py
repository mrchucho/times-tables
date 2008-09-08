#!/usr/bin/env python
#
# Copyright 2008 Ralph M. Churchill
#

import wsgiref.handlers
import os
import logging
import random

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch

from django.utils import simplejson

from stats import Stats

COOKIE_NAME = 'times-tables'

class MultiplyHandler(webapp.RequestHandler):
	__TEMPLATE_PATH = os.path.join(os.path.dirname(__file__),'templates')
	__TEMPLATE = os.path.join(__TEMPLATE_PATH,'index.html')

	def __is_ajax(self):
		return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

	def __wants_json(self):
		return any(map(lambda h: h == 'application/json',self.request.headers.get('Accept','').split(',')))

	def __read_stats(self):
		stats = Stats()
		stats.correct,stats.incorrect,stats.questions = \
				map(lambda c: int(c),self.request.cookies.get(COOKIE_NAME,'0,0,0').split(','))
		return stats

	def __write_stats(self,stats):
		self.response.headers.add_header('Set-Cookie', \
				"%s=%d,%d,%d;" % (COOKIE_NAME,stats.correct,stats.incorrect,stats.questions))

	def post(self):
		stats = self.__read_stats()
		try:
			l,r,ans = map(lambda p: int(self.request.get(p) or '-1'),['l','r','a'])
		except ValueError:
			self.error(400)
			return
		if l * r == ans:
			stats.right()
			self.__write_stats(stats)
			if self.__is_ajax():
				l = random.randrange(0,12)
				r = random.randrange(0,12)
				self.response.out.write(simplejson.dumps([{'l':l,'r':r}, stats.to_hash()]))
			else:
				self.redirect('/')
		else:
			msg = 'Sorry, that was wrong'
			stats.wrong()
			self.__write_stats(stats)
			if self.__is_ajax():
				self.response.out.write(simplejson.dumps([{'l':l,'r':r,'msg':msg},stats.to_hash()]))
			else:
				self.response.out.write(template.render(self.__TEMPLATE,{
					'l': l,'r': r,'stats':stats,
					'msg':msg,
					}))

	def get(self):
		stats = self.__read_stats()
		l = random.randrange(0,12)
		r = random.randrange(0,12)
		if self.__is_ajax():
			self.response.out.write(simplejson.dumps([{'l':l,'r':r},stats.to_hash()]))
		else:
			self.response.out.write(template.render(self.__TEMPLATE,{
				'l': l,'r': r,'stats':stats,
				}))


class ResetHandler(webapp.RequestHandler):
	def get(self):
		self.response.headers.add_header('Set-Cookie','%s=0,0,0' % COOKIE_NAME)
		self.redirect('/')


def main():
	application = webapp.WSGIApplication([('/reset',ResetHandler),('/', MultiplyHandler)],debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()
