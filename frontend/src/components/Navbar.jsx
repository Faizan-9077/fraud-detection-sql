import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Chip,
} from "@mui/material";

import SecurityIcon from "@mui/icons-material/Security";

export default function Navbar() {
  return (
    <AppBar
      position="static"
      elevation={2}
      sx={{
        backgroundColor: "#1565C0",
      }}
    >
      <Toolbar
        sx={{
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        {/* Left Side */}
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 2,
          }}
        >
          <SecurityIcon sx={{ fontSize: 38 }} />

          <Box>
            <Typography
              variant="h6"
              sx={{
                fontWeight: 700,
              }}
            >
              AML Fraud Detection & Compliance Reporting
            </Typography>

            <Typography
              variant="body2"
              sx={{
                opacity: 0.9,
              }}
            >
              Natural Language → SQL Investigation System
            </Typography>
          </Box>
        </Box>

        {/* Right Side */}
        <Chip
          label="API Connected"
          color="success"
          variant="filled"
        />
      </Toolbar>
    </AppBar>
  );
}