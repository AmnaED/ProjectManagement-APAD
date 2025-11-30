from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
from project import Project
import os

# Load environment variables from .env
load_dotenv()

# Initialize Flask App
app = Flask(__name__, static_folder='/client/build', static_url_path='')
# Note: session/secret_key is no longer needed but kept the basic setup
app.secret_key = os.getenv("SECRET_KEY")
CORS(app, supports_credentials=True)


# Get MongoDB password and connect to database
mongo_pass = os.getenv("MONGO_PASSWORD")
# Only project-related connection details are strictly necessary
link = f"mongodb+srv://ranyae:{mongo_pass}@apad-project.qvgsgr3.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(link)

# Accessing the project collection only
project_db = client["project-table-db"]
project_collection = project_db["project-table"]


## Project Management Routes 🛠️

@app.route("/")
def home():
    """Simple health check route."""
    return jsonify({"message": "Project Management Service running!"})

# ---
# Project Creation and Retrieval

@app.route("/projects", methods=["POST"])
def create_project():
    """Creates a new project and stores it in the database."""
    data = request.get_json()
    # It's better to use an auto-generated ID in a real app, but keeping the original structure
    try:
        project_id = int(data.get("project_id"))
    except (ValueError, TypeError):
        return jsonify({"error": "Valid Project ID is required"}), 400

    project_name = data.get("project_name")
    project_description = data.get("project_description")

    if not project_id or not project_name:
        return jsonify({"error": "Missing required fields (project_id, project_name)"}), 400

    if project_collection.find_one({"project_id": project_id}):
        return jsonify({"error": "Project ID already exists"}), 400

    # Project class must be available (imported from 'project')
    new_project = Project(project_id=project_id, project_name=project_name, project_description=project_description)
    project_collection.insert_one(new_project.to_dict())
    
    return jsonify({"message": "Project created successfully", "project_id": project_id}), 201

@app.route("/projects", methods=["GET"])
def get_projects():
    # example: return all projects from Mongo
    projects = list(project_collection.find({}, {"_id": 0}))
    return jsonify({"projects": projects}), 200

@app.route("/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):
    """Retrieves project details by project ID."""
    # Exclude _id from result
    project_data = project_collection.find_one({"project_id": project_id}, {"_id": 0})
    if project_data:
        # Project class must be available (imported from 'project')
        project = Project(project_data=project_data)
        return jsonify(project.to_dict())
    else:
        return jsonify({"error": "Project not found"}), 404

# ---
# Project Member Management

@app.route("/projects/<int:project_id>/users", methods=["POST"])
def add_user_to_project(project_id):
    """Adds a user (by user_id) to the specified project's members list."""
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing user ID"}), 400

    project_data = project_collection.find_one({"project_id": project_id})
    if not project_data:
        return jsonify({"error": "Project not found"}), 404

    # Project class must be available (imported from 'project')
    project = Project(project_data=project_data)
    if user_id in project.get_members():
        return jsonify({"error": "User already in project"}), 400

    project.add_user(user_id)
    # Update only the user_ids field
    project_collection.update_one({"project_id": project_id}, {"$set": {"user_ids": project.get_members()}})
    return jsonify({"message": "User added to project successfully"}), 200

@app.route("/projects/<int:project_id>/users/<string:user_id>", methods=["DELETE"])
def remove_user_from_project(project_id, user_id):
    """Removes a user (by user_id) from the specified project's members list."""
    project_data = project_collection.find_one({"project_id": project_id})
    if not project_data:
        return jsonify({"error": "Project not found"}), 404

    # Project class must be available (imported from 'project')
    project = Project(project_data=project_data)
    if user_id not in project.get_members():
        return jsonify({"error": "User not in project"}), 404
    
    project.remove_user(user_id)
    # Update only the user_ids field
    project_collection.update_one({"project_id": project_id}, {"$set": {"user_ids": project.get_members()}})
    return jsonify({"message": "User removed from project successfully"}), 200

@app.route("/projects/<int:project_id>/members", methods=["GET"])
def get_project_members(project_id):
    """Retrieves the list of user IDs (members) associated with a project."""
    # Exclude _id from result
    project_data = project_collection.find_one({"project_id": project_id}, {"_id": 0})
    if not project_data:
        return jsonify({"error": "Project not found"}), 404

    # Return the user_ids list, defaulting to an empty list if not present
    members = project_data.get("user_ids", [])
    return jsonify({"members": members})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
