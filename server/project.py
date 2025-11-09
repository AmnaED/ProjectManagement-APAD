# project.py
# class definition for Projects
# manage users in each project

class Project:
    def __init__(self, project_data = None, project_id = None, project_name = None, project_description = None):
        if project_data:        # if project document is passed in from database (in dict format)
            self.__project_id = project_data.get("project_id", 0)
            self.__project_name = project_data.get("project_name", "")
            self.__project_description = project_data.get("project_description", "")
            self.__members = project_data.get("user_ids", []) # list of userID strings - multiple user ids for one proj, blank list if no ids stored yet
        else:
            self.__project_id = project_id
            self.__project_name = project_name
            self.__project_description = project_description
            self.__members = []

    def add_user(self, user_id): 
        if user_id not in self.__members:
            self.__members.append(user_id)
    
    def remove_user(self, user_id):
        if user_id in self.__members:
            self.__members.remove(user_id)

    def get_members(self):
        return self.__members

    def get_project_id(self):
        return self.__project_id

    def get_project_name(self):
        return self.__project_name

    def get_project_description(self):
        return self.__project_description
    
    def to_dict(self):
        return {
            "project_id": self.__project_id,
            "project_name": self.__project_name,
            "project_description": self.__project_description,
            "user_ids": self.__members
        }
