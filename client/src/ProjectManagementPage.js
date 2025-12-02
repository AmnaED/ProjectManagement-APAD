import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import API_BASE_URL from './config';

function ProjectManagementPage() {
  const { project_id } = useParams();
  const [project, setProject] = useState(null);
  const [members, setMembers] = useState([]);
  const [userIdToAdd, setUserIdToAdd] = useState('');
  const [loading, setLoading] = useState(true);

  // Fetch project details
  useEffect(() => {
    fetchProjectDetails();
    fetchProjectMembers();
  }, [project_id]);

  async function fetchProjectDetails() {
    try {
      const response = await fetch(`${API_BASE_URL}/projects/${project_id}`);
      const data = await response.json();
      if (response.ok) {
        setProject(data);
      } else {
        alert(data.error || 'Error fetching project details');
      }
    } catch (error) {
      console.error('Error fetching project:', error);
      alert('Error fetching project details');
    } finally {
      setLoading(false);
    }
  }

  async function fetchProjectMembers() {
    try {
      const response = await fetch(`${API_BASE_URL}/projects/${project_id}/members`);
      const data = await response.json();
      if (response.ok) {
        setMembers(data.members || []);
      } else {
        alert(data.error || 'Error fetching members');
      }
    } catch (error) {
      console.error('Error fetching members:', error);
    }
  }

  async function handleAddUser(event) {
    event.preventDefault();
    if (!userIdToAdd.trim()) {
      alert('Please enter a user ID');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/projects/${project_id}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userIdToAdd }),
      });
      const data = await response.json();
      
      if (response.ok) {
        alert(data.message);
        setUserIdToAdd('');
        fetchProjectMembers();
      } else {
        alert(data.error || 'Error adding user');
      }
    } catch (error) {
      console.error('Error adding user:', error);
      alert('Error adding user to project');
    }
  }

  async function handleRemoveUser(userId) {
    if (!window.confirm(`Remove user ${userId} from project?`)) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/projects/${project_id}/users/${userId}`, {
        method: 'DELETE',
      });
      const data = await response.json();
      
      if (response.ok) {
        alert(data.message);
        fetchProjectMembers();
      } else {
        alert(data.error || 'Error removing user');
      }
    } catch (error) {
      console.error('Error removing user:', error);
      alert('Error removing user from project');
    }
  }

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!project) {
    return <div>Project not found</div>;
  }

  return (
    <div>
      <h1>Project Management</h1>
      
      <div>
        <h2>Project Details</h2>
        <p><strong>Project ID:</strong> {project.project_id}</p>
        <p><strong>Project Name:</strong> {project.project_name}</p>
        <p><strong>Description:</strong> {project.project_description}</p>
      </div>

      <div>
        <h2>Project Members</h2>
        {members.length === 0 ? (
          <p>No members in this project yet.</p>
        ) : (
          <ul>
            {members.map((memberId) => (
              <li key={memberId}>
                {memberId}{' '}
                <button onClick={() => handleRemoveUser(memberId)}>Remove</button>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div>
        <h2>Add User to Project</h2>
        <form onSubmit={handleAddUser}>
          <label>
            User ID:
            <input
              type="text"
              value={userIdToAdd}
              onChange={(e) => setUserIdToAdd(e.target.value)}
            />
          </label>
          <br />
          <button type="submit">Add User</button>
        </form>
      </div>
    </div>
  );
}

export default ProjectManagementPage;