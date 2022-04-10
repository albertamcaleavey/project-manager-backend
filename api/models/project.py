from datetime import datetime
from api.models.db import db

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    deadline = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    def __repr__(self):
      return f"Project('{self.id}', '{self.name}'"

    def serialize(self):
      project = {c.name: getattr(self, c.name) for c in self.__table__.columns}
      return project