from flask import Flask, jsonify, request, session
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
from hardware import hardwareSet
from user import User
from project import Project
import os

# Load environment variables from .env
load_dotenv()

## needed N and D values
N = int(os.getenv("N"))
D = int(os.getenv("D"))

# Initialize hardware set
hardware_set = hardwareSet()

app = Flask(__name__, static_folder='/client/build', static_url_path='')
app.secret_key = os.getenv("SECRET_KEY")
CORS(app, supports_credentials=True)


# Get MongoDB password and connect to database
mongo_pass = os.getenv("MONGO_PASSWORD")
link = f"mongodb+srv://ranyae:{mongo_pass}@apad-project.qvgsgr3.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(link)

# Accessing collections
resource_db = client["resource-management-db"]
resources_collection = resource_db["resources"]
project_db = client["project-table-db"]
project_collection = project_db["project-table"]
user_db = client["user-management-db"]
user_collection = user_db["user-management"]


@app.route("/")
def home():
    return jsonify({"message": "Hello from Flask!"})

        
@app.route("/hardware/<int:hardware_id>/capacity", methods=["GET"])
def get_hardware_capacity(hardware_id):
    hardware = resources_collection.find_one(
        {"hardware_id": hardware_id},
        {"_id": 0, "total_capacity": 1}
    )
    if hardware:
        hardware["hardware_id"] = hardware_id  # Add hardware_id to the dict
        hardware_set.initialize_capacity(hardware)
        capacity = hardware_set.get_capacity()
        return jsonify({"capacity": capacity})

    return jsonify({"error": "Hardware not found"}), 404


@app.route("/hardware/<int:hardware_id>/availability", methods=["GET"])
def get_hardware_availability(hardware_id):
    hardware = resources_collection.find_one(
        {"hardware_id": hardware_id},
        {"_id": 0, "available": 1}
    )
    if hardware:
        hardware["hardware_id"] = hardware_id  # Add hardware_id to dict
        hardware_set.initialize_availability(hardware)
        availability = hardware_set.get_availability()
        return jsonify({"availability": availability})

    return jsonify({"error": "Hardware not found"}), 404


    
@app.route("/hardware/checkout", methods=["POST"])
def checkout_hardware():
    data = request.get_json()
    qty = data.get("qty")
    project_id = data.get("project_id")
    hardware_id = data.get("hardware_id")

    result, updated_availability = hardware_set.check_out(qty, project_id, hardware_id)

    hardware = resources_collection.find_one({"hardware_id": hardware_id})
    if not hardware:
        return jsonify({"error": "Hardware not found"}), 400

    resources_collection.update_one(
        {"hardware_id": hardware_id},
        {"$set": {"available": updated_availability}}
    )

    if result == -1:
        return jsonify({"error": "No units available for checkout"}), 400
    elif result == 1:
        return jsonify({
            "message": "Only partial checkout completed.",
            "available": updated_availability
        }), 200
    elif result == 0:
            return jsonify({
                "message": "Checkout successful.",
                "available": updated_availability
            }), 200
    else:
        return jsonify({
            "message": "Unexpected checkout case.",
            "available": updated_availability
        }), 500

@app.route("/hardware/checkin", methods=["POST"])
def checkin_hardware():
    data = request.get_json()
    qty = data.get("qty")
    project_id = data.get("project_id")
    hardware_id = data.get("hardware_id")

    result, updated_availability = hardware_set.check_in(qty, project_id, hardware_id)

    if result in [0, 1]:  # Only update DB if any check-in actually occurred
        resources_collection.update_one(
            {"hardware_id": hardware_id},
            {"$set": {"available": updated_availability}}
        )

    if result == -1:
        return jsonify({"error": "Project never checked anything out."}), 400
    elif result == -2:
        return jsonify({"error": "Nothing to check in for this project and hardware."}), 400
    elif result == -3:
        return jsonify({"error": "You cannot check in hardware more than capacity."}), 400
    elif result == -4:
        return jsonify({"error": "You cannot check in < 0"}), 400
    elif result == 1:
        return jsonify({
            "message": "Partial check-in completed. Some units not accepted to avoid overfilling.",
            "available": updated_availability
        }), 200
    elif result == 0:
        return jsonify({
            "message": "Check-in successful.",
            "available": updated_availability
        }), 200
    else:
        return jsonify({"error": "Unexpected error during check-in."}), 500

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user_id = data.get("user_id")
    name = data.get("name")
    password = data.get("password")

    if not user_id or not name or not password:
        return jsonify({"error": "Missing required fields"}), 400

    if user_collection.find_one({"user_id": user_id}):
        return jsonify({"error": "User already exists"}), 400
    
    new_user = User(user_id=user_id, name=name, password=password, N=N, D=D)
    user_collection.insert_one(new_user.to_dict())
    return jsonify({"message": "User created successfully"}), 201


@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    logged_in_user = session.get("user_id")
    if not logged_in_user:
        return jsonify({"error": "Unauthorized: Please log in"}), 401
    user_data = user_collection.find_one({"user_id": user_id}, {"_id": 0})
    if user_data:
        user = User(user_data=user_data, encrypted=True)
        return jsonify(user.to_dict())
    else:
        return jsonify({"error": "User not found"}), 404

@app.route("/users/<user_id>/projects", methods=["POST"])
def add_user_to_project(user_id):
    data = request.get_json()
    project_id = int(data.get("project_id"))

    if not project_id:
        return jsonify({"error": "Project ID is required"}), 400

    user_data = user_collection.find_one({"user_id": user_id})
    if not user_data:
        return jsonify({"error": "User not found"}), 404

    user = User(user_data=user_data, encrypted=True)
    user.add_to_project(project_id)
    user_collection.update_one({"user_id": user_id}, {"$set": user.to_dict()})
    
    return jsonify({"message": "User added to project successfully"}), 200

@app.route("/users/<user_id>/projects", methods=["DELETE"])
def remove_user_from_project(user_id):
    data = request.get_json()
    project_id = int(data.get("project_id"))

    if not project_id:
        return jsonify({"error": "Project ID is required"}), 400
        
    user_data = user_collection.find_one({"user_id": user_id})
    if not user_data:
        return jsonify({"error": "User not found"}), 404

    user = User(user_data=user_data, encrypted=True)
    user.remove_from_project(project_id)
    user_collection.update_one({"user_id": user_id}, {"$set": user.to_dict()})
    
    return jsonify({"message": "User removed from project successfully"}), 200

@app.route("/projects", methods=["POST"])
def create_project():
    data = request.get_json()
    project_id = int(data.get("project_id"))
    project_name = data.get("project_name")
    project_description = data.get("project_description")

    if not project_id or not project_name:
        return jsonify({"error": "Missing required fields"}), 400

    if project_collection.find_one({"project_id": project_id}):
        return jsonify({"error": "Project ID already exists"}), 400

    new_project = Project(project_id=project_id, project_name=project_name, project_description=project_description)
    project_collection.insert_one(new_project.to_dict())
    
    return jsonify({"message": "Project created successfully", "project_id": project_id}), 201

@app.route("/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):
    project_data = project_collection.find_one({"project_id": project_id}, {"_id": 0})
    if project_data:
        project = Project(project_data=project_data)
        return jsonify(project.to_dict())
    else:
        return jsonify({"error": "Project not found"}), 404

@app.route("/projects/<int:project_id>/users", methods=["POST"])
def add_user_to_project_2(project_id):
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing user ID"}), 400

    project_data = project_collection.find_one({"project_id": project_id})
    if not project_data:
        return jsonify({"error": "Project not found"}), 404

    project = Project(project_data=project_data)
    if user_id in project.get_members():
        return jsonify({"error": "User already in project"}), 400

    project.add_user(user_id)
    project_collection.update_one({"project_id": project_id}, {"$set": {"user_ids": project.get_members()}})
    return jsonify({"message": "User added to project successfully"}), 200

@app.route("/projects/<int:project_id>/users/<string:user_id>", methods=["DELETE"])
def remove_user_from_project_2(project_id, user_id):
    project_data = project_collection.find_one({"project_id": project_id})
    if not project_data:
        return jsonify({"error": "Project not found"}), 404

    project = Project(project_data=project_data)
    if user_id not in project.get_members():
        return jsonify({"error": "User not in project"}), 404
    
    project.remove_user(user_id)
    project_collection.update_one({"project_id": project_id}, {"$set": {"user_ids": project.get_members()}})
    return jsonify({"message": "User removed from project successfully"}), 200

@app.route("/projects/<int:project_id>/members", methods=["GET"])
def get_project_members(project_id):
    project_data = project_collection.find_one({"project_id": project_id}, {"_id": 0})
    if not project_data:
        return jsonify({"error": "Project not found"}), 404

    members = project_data.get("user_ids", [])
    return jsonify({"members": members})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get("user_id")
    password = data.get("password")

    if not user_id or not password:
        return jsonify({"error": "Missing required fields"}), 400
    user_data = user_collection.find_one({"user_id": user_id}, {"_id": 0})
    if not user_data:
        return jsonify({"error": "User not found"}), 404
    user = User(user_data=user_data, encrypted=True, N=N, D=D)
    if not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    session["user_id"] = user_id
    return jsonify(user.to_dict())

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200



if __name__ == "__main__":
    app.run(debug=True)