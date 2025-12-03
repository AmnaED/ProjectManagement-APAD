import React, {useState} from "react";
import { useNavigate } from 'react-router-dom';
import { useParams } from 'react-router-dom';
import API_BASE_URL from './config';
import './ProjectForm.css';



function ProjectForm(props) {
  const navigate = useNavigate();
  const { user_id: urlUserId } = useParams();
  const [formData, setFormData] = useState({
    user_id: urlUserId || '',
    project_id: '',
    project_name: '',
    project_description: '',
  });

  function handleInputChange(event) {
    const { name, value } = event.target;

    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  }

  // add user to project
  async function addUser(project_id) {

    try {
      const response = await fetch (`${API_BASE_URL}/projects/${Number(project_id)}/users`, {
        method: "POST",
        headers: {"Content-Type" : "application/json"},
        body: JSON.stringify({user_id: formData.user_id,}),
      });
      const data = await response.json();
      console.log("Data recieved", data.message);

      if (response.ok) {
        console.log("User added to project");
        return response;
      } else {
        alert(data.error || "Error in adding user to project");
        return response;
      }
    } catch (error) {
      console.error("Error adding user to project:", error);
      alert("Error adding user to project.");
    }
  }

  // add project to user
  async function addProject(user_id, project_id) {

    try {
      const response = await fetch (`${API_BASE_URL}/users/${user_id}/projects`, {
        method: "POST",
        headers: {"Content-Type" : "application/json"},
        body: JSON.stringify({project_id: Number(project_id)}),
      });
      const data = await response.json();
      console.log("Data recieved", data.message);

      if (response.ok) {
        console.log("Project added to User");
        return response;
      } else {
        alert(data.error || "Error in adding project to user");
        return response;
      }
    } catch (error) {
      console.error("Error adding project to user:", error);
      alert("Error adding project to user.");
    }
  }


  async function handleSubmit(event) {
        
    event.preventDefault();
    console.log("Form Submitted", formData);

    // Validate that user_id is provided
    if (!formData.user_id) {
      alert("Please enter a User ID");
      return;
    }

    // Create new project and immediately link user and project
    try {
        const response = await fetch(`${API_BASE_URL}/projects`,{
        method: "POST",
        headers: {"Content-Type" : "application/json"},
        body: JSON.stringify(formData),
        });
        const data = await response.json();
        console.log("Data recieved from Flask", data);
        
        if (!response.ok) {
          alert(data.error || data.message);
          return;
        }  
          // automatically link project and user 
          const projectId = data.project_id;
          const projectName = formData.project_name || "Unnamed Project";
          const userId = formData.user_id;
          
          const addUserResponse = await addUser(projectId);
          const addProjectResponse = await addProject(userId, projectId);
          
          if (addUserResponse?.ok && addProjectResponse?.ok) {
            // reset form inputs
            setFormData({ user_id: '', project_id: '', project_name: '', project_description: '' });
            alert(`✓ Success! New project created:\n\nProject Name: ${projectName}\nProject ID: ${projectId}\nUser ID: ${userId}\n\nThe project has been successfully linked to the user.`);
            navigate(`/resource-management`);  // navigate to resource page
          } else if (addUserResponse?.ok && !addProjectResponse?.ok) {
            console.log("User added to project, error adding project to user.");
            alert(`✓ Project "${projectName}" (ID: ${projectId}) has been created!\n\nUser was added to project successfully.`);
            navigate(`/resource-management`);  // navigate to resource page
          } else if (!addUserResponse?.ok && addProjectResponse?.ok) {
            console.log("Project added to user, user already in project.");
            alert(`✓ Project "${projectName}" (ID: ${projectId}) has been created!\n\nProject was added to user successfully.`);
            navigate(`/resource-management`);  // navigate to resource page
          } else {
            alert(`⚠ Project "${projectName}" (ID: ${projectId}) has been created, but there was an issue linking it with the user.\n\nCheck console for details.`);
          }
        } catch (error) {
          console.error("Error submitting form:", error);
          alert("An error occurred while creating the project. Please try again.");
        }
  }
return(

    <form onSubmit={handleSubmit}>
        <h2>Create a New Project</h2>
        <label>
            User ID: 
            <input name = "user_id" type = "number" value = {formData.user_id} onChange =  {handleInputChange} required/>
        </label>
        <br />
        <label>
            Project Name: 
            <input name = "project_name" value = {formData.project_name} onChange =  {handleInputChange}/>
        </label>
        <br />
        <label>
            Project Description:
            <input name = "project_description" value = {formData.project_description} onChange = {handleInputChange}/>
        </label>
        <br />
        <label>
            Project ID:
            <input name = "project_id" type = "number" value = {formData.project_id} onChange = {handleInputChange}/>
        </label>
            <br />
        <button type="submit">Create Project</button>
    </form>
    );
}
export default ProjectForm;