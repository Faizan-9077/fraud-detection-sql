import { useState } from "react";

import {
  Box,
  TextField,
  Button,
  CircularProgress,
} from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";


export default function QueryInput({
    question,
    setQuestion,
    runQuery,
}) {

  const [loading, setLoading] = useState(false);

  

const handleSearch = async () => {
    if (!question.trim()) return;

    try {
        setLoading(true);

        await runQuery(question);

    } finally {
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