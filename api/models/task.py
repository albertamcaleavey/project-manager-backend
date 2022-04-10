from datetime import datetime
from sqlite3 import dbapi2
from api.models.db import db

class Task(db.Model):
  __tablename__ = 'tasks'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String)
  date = db.Column(db.Date)
  created_at = db.Column(db.DateTime, default=datetime.now(tz=None))
  project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

  def __repr__(self):
      return f"Task('{self.id}'"

  def serialize(self):
    return {
      "id": self.id,
      "project_id": self.project_id,
      "description": self.description,
      "date": self.date
    }

