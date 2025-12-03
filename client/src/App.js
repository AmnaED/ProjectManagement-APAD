import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import ProjectForm from './ProjectForm';

function App() {
  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<ProjectForm />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;