import axios from "axios";

// Adjust if needed – this should match your FastAPI user_service
const API = axios.create({
  baseURL: "http://localhost:8001/api/users",
});

// LOGIN – FastAPI expects form-data (OAuth2PasswordRequestForm)
export const loginUser = (formData) =>
  API.post("/login", formData, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

// REGISTER – JSON body
export const registerUser = (data) => API.post("/", data);
