#!/usr/bin/python
# -*- coding: utf8 -*- 

import os.path

import cherrypy, simplejson
from mako.template import Template
from mako.lookup import TemplateLookup

class Root(object):

	def __init__(self):
		self.lookup = TemplateLookup(directories=['html'])

	@cherrypy.expose
	def index(self):
		print cherrypy.request.method
		tmpl = self.lookup.get_template("index.html")
		return tmpl.render(salutation="Hello", target="World")

	@cherrypy.expose
	@cherrypy.tools.json_out(on = True)
	def update(self):
		success = False
		cl = cherrypy.request.headers['Content-Length']
		rawbody = cherrypy.request.body.read(int(cl))

		print "'",rawbody,"'"

		if len(rawbody) > 0:
			body = simplejson.loads(rawbody)
			print "'",body,"'"

			if body["command"] == 'status':
				success = True

		return { 'success': success }

if __name__ == '__main__':
	current_dir = os.path.dirname(os.path.abspath(__file__))

	# Set up site-wide config first so we get a log if errors occur.
	cherrypy.config.update({
		#'environment': 'production',
		'log.error_file': 'logs/site.log',
		'log.screen': True
	})

	conf = {
		'global': {
		#	'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			"request.methods_with_bodies": ("POST", "PUT", "PROPPATCH")
		},
		'/update': {
			"request.methods_with_bodies": ("POST", "GET", "PUT", "PROPPATCH")
		},
		'/css': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': os.path.join(current_dir, 'css'),
			'tools.staticdir.content_types': { 'css': 'text/css' }
		},
		'/js': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': os.path.join(current_dir, 'js'),
			'tools.staticdir.content_types': { 'css': 'text/javascript' }
		},
		'/img': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': os.path.join(current_dir, 'img'),
			'tools.staticdir.content_types': {
				'png': 'image/png',
				'jpg': 'image/jpg'
			}
		}
	}
	cherrypy.quickstart(Root(), '/', config=conf)