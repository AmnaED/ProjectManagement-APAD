import React from "react";
import { useNavigate } from "react-router-dom";

function Logout() {
    const navigate = useNavigate();
    async function handleLogout () {
        try {
            const response = await fetch ("http://localhost:5000/logout", {
                method: "POST",
                credentials: "include",
            });
           if (response.ok) {
            alert("Logged out successfully");
            navigate("/");
           } else {
            alert("Error logging out");
           }
        } catch (error) {
            alert("Logout error");
        }
    }
  return (
    <button onClick={handleLogout}>
      Logout
    </button>
  );
}

export default Logout;