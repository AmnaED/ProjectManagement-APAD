import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import ProjectManagementPage from './ProjectManagementPage';

function App() {
  return (
    <div>
      <Router>
        <Routes>
          <Route path="/project-management/:project_id" element={<ProjectManagementPage />} />
          <Route path="/" element={<Navigate to="/project-management/204" replace />} />
          <Route path="/project-management" element={<Navigate to="/project-management/204" replace />}/>
        </Routes>
      </Router>
    </div>
  );
}

export default App;