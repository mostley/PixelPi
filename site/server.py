#!/usr/bin/python
# -*- coding: utf8 -*- 

import os.path

import cherrypy, simplejson
from mako.template import Template
from mako.lookup import TemplateLookup

class Root(object):

    def __init__(self):
        self.lookup = TemplateLookup(directories=['html'])

        self.currentMode = 'pong'
        self.modules = {}

        self.validCommands = []

    @cherrypy.expose
    def index(self):
        print cherrypy.request.method
        tmpl = self.lookup.get_template("index.html")
        return tmpl.render(salutation="Hello", target="World")

    def setMode(self, mode):
        self.currentMode = mode

        if not self.modules.has_key(mode):
            self.modules[mode] = __import__(mode)

        if self.modules.has_key(mode) and self.modules[mode]:
            self.currentModule = self.modules[mode]

            self.currentModule.init()
            self.validCommands = self.currentModule.commands

    def executeCommand(self, data):
        result = False
        if self.currentModule:
            result = self.currentModule.execute(data)
        return result

    @cherrypy.expose
    @cherrypy.tools.json_out(on = True)
    def update(self):
        result = { 'success': False, 'command': '' }
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))

        print "'",rawbody,"'"

        if len(rawbody) > 0:
            body = simplejson.loads(rawbody)
            print "'",body,"'"

            result['command'] = body["command"]

            if body["command"] == 'status':
                result['success'] = True
                result['mode'] = self.currentMode
            
            elif body["command"] == 'changemode':
                self.setMode(body['mode'])
                result['mode'] = body['mode']

            elif body["command"] in self.validCommands:
                result['success'] = self.executeCommand(data)

        return result

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Set up site-wide config first so we get a log if errors occur.
    cherrypy.config.update({
        #'environment': 'production',
        'server.socket_host': '192.168.1.5',
        'server.socket_port': 8080,
        'log.error_file': 'logs/site.log',
        'log.screen': True
    })

    conf = {
        'global': {
        #   'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
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
