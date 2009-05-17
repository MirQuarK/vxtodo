import os
import time

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.db import Key
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from datamodel import *

dirs = {
    "template":"template/"
}

class Index(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        login = 0
        if user is not None:
            login = 1
        template_values = {
            'login' : login
        }
        path = os.path.join(os.path.dirname(__file__), dirs['template'] + 'index.html')
        self.response.out.write(template.render(path, template_values))

class Prism(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        login = 0
        if user is not None:
            login = 1
        template_values = {
            'login' : login
        }
        path = os.path.join(os.path.dirname(__file__), dirs['template'] + 'prism.html')
        self.response.out.write(template.render(path, template_values))

class Board(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user is None:
            self.redirect("/")

        template_values = {
            "user" : user.nickname(),
            "useremail" : user.email()
        }
        path = os.path.join(os.path.dirname(__file__), dirs['template'] + 'board.html')
        self.response.out.write(template.render(path, template_values))

class Action_Update(webapp.RequestHandler):
    def get(self):
        self.redirect("/board.vx")
    def post(self):
        user = users.get_current_user()

        if user is None:
            self.redirect("/")

        query = Task.all()
        query.filter("user = ", user)
        query.order("-createtime")

        template_values = {
            "items" : query.fetch(1000)
        }

        path = os.path.join(os.path.dirname(__file__), dirs['template'] + 'items.js')
        self.response.out.write(template.render(path, template_values))


class Action_Add(webapp.RequestHandler):
    def get(self):
        self.redirect("/board.vx")
    def post(self):
        user = users.get_current_user()

        if user is None:
            self.redirect("/")

        task = Task()
        task.user = user
        task.title = self.request.get("title")
        task.content = self.request.get("content")
        task.color = int(self.request.get("color"))
        task.createtime = int(time.time())

        task.remindtime = int(self.request.get("remindtime"))
        if task.remindtime != 0:
            task.email = self.request.get("email")

        task.put()

class Action_Edit(webapp.RequestHandler):
    def get(self):
        self.redirect("/board.vx")
    def post(self):
        user = users.get_current_user()

        if user is None:
            self.redirect("/")

        taskid = int(self.request.get("id"))
        key = Key.from_path("Task", taskid)

        query = Task.all()
        query.ancestor(key)
        task = query.get()
        
        task.title = self.request.get("title")
        task.content = self.request.get("content")
        task.color = int(self.request.get("color"))
        task.status = int(self.request.get("status"))
        if task.status == 1:
            task.endtime = int(time.time())

        task.remindtime = int(self.request.get("remindtime"))
        if task.remindtime != 0:
            task.email = self.request.get("email")
        
        db.put(task)

class Action_Status(webapp.RequestHandler):
    def get(self):
        self.redirect("/board.vx")
    def post(self):
        user = users.get_current_user()

        if user is None:
            self.redirect("/")

        taskid = int(self.request.get("id"))
        key = Key.from_path("Task", taskid)

        query = Task.all()
        query.ancestor(key)
        task = query.get()

        task.status = int(self.request.get("status"))
        if task.status == 1:
            task.endtime = int(time.time())
        else:
            task.endtime = 0
        
        db.put(task);
        
        template_values = {
            "items" : [task]
        }
        path = os.path.join(os.path.dirname(__file__), dirs['template'] + 'items.js')
        self.response.out.write(template.render(path, template_values))


class Action_Del(webapp.RequestHandler):
    def get(self):
        self.redirect("/board.vx")
    def post(self):
        user = users.get_current_user()

        if user is None:
            self.redirect("/")
        
        taskid = int(self.request.get("id"))
        key = Key.from_path("Task", taskid)

        db.delete(key)

application = webapp.WSGIApplication(
                                     [('/', Index),
                                      ('/index', Index),
                                      ('/prism', Prism),
                                      ('/board.vx', Board),
                                      ('/update.vx', Action_Update),
                                      ('/add.vx', Action_Add),
                                      ('/edit.vx', Action_Edit),
                                      ('/status.vx', Action_Status),
                                      ('/del.vx', Action_Del),
                                      ],
                                     debug=True)



def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()