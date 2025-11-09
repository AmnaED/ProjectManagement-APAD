
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from './Navbar';
import UserPage from './UserPage';
import ProjectPage from './ProjectPage';
import ResourceManagementPage from './ResourceManagementPage';
import Logout from './Logout';




function App() {
  return (
    <div>
      <Router>
        <Navbar />
        <Routes>
          <Route path = "/" element ={<UserPage />} />
          <Route path="/users/:user_id/projects/" element={<ProjectPage />} />
          {/*<Route path="/resource-management" element={<ProjectPage />} /> */}
          <Route path="/resource-management" element={<ResourceManagementPage />} />
          {/*<Route path="/resource-management" element={<ResourceManagementPage />} /> */}
        </Routes>

      </Router>

    </div>
  );
}

export default App;
