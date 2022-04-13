from crypt import methods
import profile
from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.project import Project
from api.models.task import Task

projects = Blueprint('projects', 'projects')


@projects.route('/', methods=["POST"])
@login_required
def create():
  data = request.get_json()
  profile = read_token(request)
  data["profile_id"] = profile["id"]
  project = Project(**data)
  db.session.add(project)
  db.session.commit()
  return jsonify(project.serialize()), 201


@projects.route('/', methods=["GET"])
def index():
  print(request)
  projects = Project.query.all()
  return jsonify([project.serialize() for project in projects]), 200


@projects.route('/<id>', methods=["GET"])
def show(id):
  project = Project.query.filter_by(id=id).first()
  project_data = project.serialize()
  return jsonify(project=project_data), 200

@projects.route('/<id>', methods=["DELETE"])
@login_required
def delete(id):
  profile = read_token(request)
  project = Project.query.filter_by(id=id).first()

  if project.profile_id != profile["id"]:
    return 'Forbidden', 403

  db.session.delete(project)
  db.session.commit()
  return jsonify(message="Success"), 200


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
