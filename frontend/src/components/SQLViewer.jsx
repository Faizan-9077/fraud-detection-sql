import {
  Paper,
  Typography,
  Box,
  IconButton,
  Tooltip,
  Divider,
} from "@mui/material";

import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import BookmarkIcon from "@mui/icons-material/Bookmark";
import { format } from "sql-formatter";

import BookmarkBorderIcon from "@mui/icons-material/BookmarkBorder";


export default function SQLViewer({
    sql,
    lastQuestion,
    toggleBookmark,
    isBookmarked,
    showSnackbar,
}) {
  const copySQL = () => {
    if (!sql) return;
    navigator.clipboard.writeText(sql);
      showSnackbar(
      "SQL copied successfully!"
  );
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Box
          sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              mb: 2,
          }}
      >

        <Typography variant="h6">

        Generated SQL

        </Typography>

        <Box sx={{ display: "flex", gap: 1 }}>

        <Tooltip title={isBookmarked ? "Remove Bookmark" : "Bookmark Investigation"}>
          <IconButton
            onClick={() => toggleBookmark(lastQuestion, sql)}
            sx={{ color: isBookmarked ? "primary.main" : "inherit" }}
          >
            {isBookmarked ? <BookmarkIcon /> : <BookmarkBorderIcon />}
          </IconButton>
        </Tooltip>

        <Tooltip title="Copy SQL">
          <IconButton onClick={copySQL}>
            <ContentCopyIcon />
          </IconButton>
        </Tooltip>

      </Box>

        </Box>

      <Divider sx={{ my: 2 }} />

      <Box
        sx={{
          bgcolor: "#1e1e1e",
          color: "#00ff90",
          p: 2,
          borderRadius: 2,
          overflowX: "auto",
          fontFamily: "monospace",
          minHeight: 140,
        }}
      >
        <pre style={{ margin: 0 }}>
          {sql
            ? format(sql, { language: "postgresql" })
            : "SQL will appear here..."}
        </pre>
      </Box>
    </Paper>
  );
}