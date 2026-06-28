import { useState } from "react";

import {
  Box,
  TextField,
  Button,
  CircularProgress,
} from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";

import api from "../services/api";

export default function QueryInput({
    setSql,
    setResults,
    setRowCount,
    setLastQuestion,
    setSuccess,
    addToHistory,
    showSnackbar,
}) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  

  const handleSearch = async () => {
    if (!question.trim()) return;

    try {
      setLoading(true);
      console.log("1. Sending request");

      const response = await api.post("/query", {
        question,
      });

      console.log("2. Response received");
      console.log(response.data);

      setSql(response.data.sql);
      console.log("3. SQL updated");

      setResults(response.data.results);
      console.log("4. Results updated");

      setRowCount(response.data.row_count);
      console.log("5. Row count updated");

      setLastQuestion(question);
      setSuccess(true);
      addToHistory(question);

    } catch (error) {
        console.error("API Error:", error);

        if (error.response) {
            console.log("Status:", error.response.status);
            console.log("Response:", error.response.data);
        }

        setSuccess(false);

        showSnackbar(
            error.response?.data?.error ||
            "Query failed.",
            "error"
        );
    
    } finally {
      console.log("6. Finally block");
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        gap: 2,
      }}
    >
      <TextField
        fullWidth
        label="Enter your AML investigation question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <Button
        variant="contained"
        startIcon={
          loading
            ? <CircularProgress size={20} color="inherit" />
            : <SearchIcon />
        }
        disabled={loading}
        onClick={handleSearch}
      >
        Search
      </Button>
    </Box>
  );
}