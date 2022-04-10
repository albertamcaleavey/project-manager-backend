from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.project import Project

projects = Blueprint('projects', 'projects')


# create a project- route
@projects.route('/', methods=["POST"])

# create controller
@login_required
def create():
  # data is a variable holding the parsed json request data
  data = request.get_json()
  # retrieve user's profile data with read_token middleware function
  profile = read_token(request)
  # add profile id property to the data (ownership)
  data["profile_id"] = profile["id"]
  # pass updated data dictionary to Project model
  project = Project(**data)
  # create the new entry in db
  db.session.add(project)
  db.session.commit()
  return jsonify(project.serialize()), 201


# indexing projects- route
@projects.route('/', methods=["GET"])

# index controller
def index():
  projects = Project.query.all()
  return jsonify([project.serialize() for project in projects]), 200

# show project- route
@projects.route('/<id>', methods=["GET"])

# show controller
def show(id):
  project = Project.query.filter_by(id=id).first()
  project_data = project.serialize()
  return jsonify(project=project_data), 200