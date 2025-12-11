import React from "react";
import { Box, Typography, Paper, Button, Grid } from "@mui/material";
import Layout from "../components/Layout";

const Dashboard = () => {
  const token = localStorage.getItem("token");

  return (
    <Layout>
      <Typography variant="h4" mb={2}>
        Meeting Room Dashboard
      </Typography>

      {!token && (
        <Typography color="error" mb={2}>
          You are not logged in. Please login to book rooms.
        </Typography>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" mb={1}>
              Quick Booking
            </Typography>
            <Typography color="text.secondary" mb={2}>
              Later you can add date/time pickers, room selection and role-based
              booking rules here.
            </Typography>
            <Button variant="contained" disabled={!token}>
              Book Room
            </Button>
          </Paper>

          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" mb={1}>
              Upcoming Meetings
            </Typography>
            <Typography color="text.secondary">
              Later, fetch upcoming bookings from booking_service and list them
              here.
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" mb={1}>
              Your Role
            </Typography>
            <Typography color="text.secondary">
              You can decode the JWT and display the user&apos;s role here
              (TEAM_LEAD, MANAGER, CEO, etc.) to customize available actions.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Layout>
  );
};

export default Dashboard;
