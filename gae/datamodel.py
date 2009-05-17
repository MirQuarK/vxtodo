from google.appengine.ext import db

class Task(db.Model):
    user = db.UserProperty()
    title = db.StringProperty()
    content = db.TextProperty()
    rank = db.IntegerProperty(default=3)
    color = db.IntegerProperty()
    createtime = db.IntegerProperty()
    endtime = db.IntegerProperty(default=0)
    email = db.StringProperty()
    remindtime = db.IntegerProperty(default=0)
    open = db.IntegerProperty(default=0)
    status = db.IntegerProperty(default=0)