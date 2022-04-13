from crypt import methods
import profile
from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.project import Project
from api.models.task import Task

projects = Blueprint('projects', 'projects')


# create a project- route
@projects.route('/', methods=["POST"])

# create controller
@login_required
def create():
  # data is a variable holding the parsed json request data
  # print(request)
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
  print(request)
  projects = Project.query.all()
  return jsonify([project.serialize() for project in projects]), 200

# show project- route
@projects.route('/<id>', methods=["GET"])

# show controller
def show(id):
  project = Project.query.filter_by(id=id).first()
  project_data = project.serialize()
  return jsonify(project=project_data), 200

# delete project - route
@projects.route('/<id>', methods=["DELETE"])

# delete controller
@login_required
def delete(id):
  profile = read_token(request)
  project = Project.query.filter_by(id=id).first()

  if project.profile_id != profile["id"]:
    return 'Forbidden', 403

  db.session.delete(project)
  db.session.commit()
  return jsonify(message="Success"), 200

#--------------------------------------------
# TASKS

# create a task - route

@projects.route('/<id>/tasks', methods=["POST"])
@login_required
def add_task(id):
  data = request.get_json()
  data["project_id"] = id

  profile = read_token(request)
  project = Project.query.filter_by(id=id).first()

  if project.profile_id != profile["id"]:
    return 'Forbidden', 403

  task = Task(**data)

  db.session.add(task)
  db.session.commit()

  project_data = project.serialize()
  
  return jsonify(project_data), 201


# @projects.route('/<id>/tasks/<taskid>', methods=["GET", "PUT"])

# @login_required
# def update(taskid):
#   data = request.get_json()
#   profile = read_token(request)
#   task = Task.query.filter_by(taskid).first()

#   if task.profile_id != profile["id"]:
#     return 'Forbidden', 403
#   for key in data:
#     setattr(task, key, data[key])

#   db.session.commit()
#   return jsonify(task.serialize()), 200