let API_BASE_URL = process.env.REACT_APP_API_URL;

// Optional override based on current hostname
if (window.location.hostname === "127.0.0.1") {
  API_BASE_URL = "http://127.0.0.1:5000";
} else if (window.location.hostname === "localhost") {
  API_BASE_URL = "http://localhost:5000";
}

export default API_BASE_URL;