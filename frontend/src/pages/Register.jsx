import React, { useState } from "react";
import {
  Box,
  Paper,
  TextField,
  Typography,
  Button,
  MenuItem,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../api/auth";

const Register = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: "",
    email: "",
    full_name: "",
    password: "",
    role: "DEVELOPER",
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await registerUser(form);
      alert("User registered successfully. Please login.");
      navigate("/");
    } catch (err) {
      console.error(err);
      alert("Registration failed. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        width: "100vw",
        height: "100vh",
        background: "linear-gradient(135deg, #1e3c72, #2a5298)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        p: 2,
      }}
    >
      <Paper
        elevation={6}
        sx={{ p: 4, width: 460, maxWidth: "100%", borderRadius: 3 }}
      >
        <Typography variant="h4" textAlign="center" mb={3}>
          Create Account
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Username"
            name="username"
            value={form.username}
            onChange={handleChange}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Full Name"
            name="full_name"
            value={form.full_name}
            onChange={handleChange}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Email"
            name="email"
            value={form.email}
            onChange={handleChange}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Password"
            name="password"
            type="password"
            value={form.password}
            onChange={handleChange}
            sx={{ mb: 2 }}
          />
          <TextField
            select
            fullWidth
            label="Role"
            name="role"
            value={form.role}
            onChange={handleChange}
            sx={{ mb: 3 }}
          >
            <MenuItem value="TEAM_LEAD">Team Lead</MenuItem>
            <MenuItem value="MANAGER">Manager</MenuItem>
            <MenuItem value="CEO">CEO</MenuItem>
            <MenuItem value="DEVELOPER">Developer</MenuItem>
            <MenuItem value="TESTER">Tester</MenuItem>
          </TextField>

          <Button type="submit" fullWidth variant="contained" disabled={loading}>
            {loading ? "Registering..." : "Register"}
          </Button>
        </form>
        <Typography
          mt={2}
          textAlign="center"
          sx={{ cursor: "pointer" }}
          onClick={() => navigate("/")}
        >
          Already have an account? Login
        </Typography>
      </Paper>
    </Box>
  );
};

export default Register;
