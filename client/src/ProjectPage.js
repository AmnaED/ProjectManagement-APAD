import ProjectForm from './ProjectForm';

function ProjectPage() {
  return (
     <div>
     <h1>Project Login Page</h1>
      <ProjectForm defaultMessage = "Enter New Project Information: " buttonMessage =  "Create Project" isNewProject={true}/>
      <ProjectForm defaultMessage = "Current/Join Project: " buttonMessage = "Join Project"/>
      
    </div>
  );
}

export default ProjectPage; 
