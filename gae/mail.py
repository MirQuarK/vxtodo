import time

from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import db

from datamodel import *


query = db.GqlQuery("SELECT * FROM Task where remindtime >= " + str(int(time.time()) - 600) + " and remindtime <= " + str(int(time.time()) + 300))

tasks = query.fetch(1000)

for task in tasks:
    mail.send_mail(sender="vxtodo.admin@gmail.com",
              to=task.email,
              subject= "[vxtodo]" + task.title,
              body=task.content + "\n\n\n==========================\nThis email was sent by program, please dont reply this email directly.\nhttp://vxtodo.ihfs.net/")
    task.remindtime = 0
    db.put(task)