import React from 'react';
import UserForm from './UserForm';
    

function UserPage() {
  return (
     <div>
     <h1>User Login Page</h1>
      <UserForm defaultMessage = "New User? Create an Account: " buttonMessage = "Create Account" isNewUser={true}/>
      <UserForm defaultMessage = "Returning User? Log In: " buttonMessage = "Log In"/>
      
    </div>
  );
}

export default UserPage; 