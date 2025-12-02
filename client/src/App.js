import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ProjectManagementPage from './ProjectManagementPage';




function App() {
  return (
    <div>
      <Router>
        <Routes>
          <Route path="/project-management/:project_id" element={<ProjectManagementPage />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;