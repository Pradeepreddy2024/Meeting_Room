import React, { useState } from "react";
import { Box, Button, TextField, Typography, Paper } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../api/auth";

const Login = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", password: "" });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const params = new URLSearchParams();
      params.append("username", form.username);
      params.append("password", form.password);

      const res = await loginUser(params);
      const token = res.data.access_token;
      localStorage.setItem("token", token);
      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      alert("Login failed. Please check your credentials.");
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
        sx={{
          width: 400,
          maxWidth: "100%",
          p: 4,
          borderRadius: 3,
          background: "rgba(255,255,255,0.1)",
          backdropFilter: "blur(10px)",
          color: "#fff",
        }}
      >
        <Typography variant="h4" textAlign="center" mb={3}>
          Welcome Back
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            name="username"
            label="Username"
            variant="outlined"
            onChange={handleChange}
            value={form.username}
            sx={{
              mb: 2,
              "& .MuiInputBase-root": {
                backgroundColor: "rgba(255,255,255,0.9)",
              },
            }}
          />
          <TextField
            fullWidth
            name="password"
            type="password"
            label="Password"
            variant="outlined"
            onChange={handleChange}
            value={form.password}
            sx={{
              mb: 3,
              "& .MuiInputBase-root": {
                backgroundColor: "rgba(255,255,255,0.9)",
              },
            }}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            disabled={loading}
            sx={{
              py: 1.5,
              background: "linear-gradient(90deg,#00c6ff,#0072ff)",
              fontSize: "1rem",
            }}
          >
            {loading ? "Logging in..." : "Login"}
          </Button>
        </form>
        <Typography
          mt={2}
          textAlign="center"
          sx={{ cursor: "pointer", color: "#e0e0e0" }}
          onClick={() => navigate("/register")}
        >
          Don&apos;t have an account? Register
        </Typography>
      </Paper>
    </Box>
  );
};

export default Login;
