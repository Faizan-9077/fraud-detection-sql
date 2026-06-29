import {
  Box,
  Typography,
  Divider,
} from "@mui/material";

import HistoryPanel from "./HistoryPanel";
import BookmarkPanel from "./BookmarkPanel";

export default function Sidebar({
    history,
    bookmarks,
    runQuery,
    setCurrentQuestion,
}) {
  return (
    <Box
      sx={{
        width: 280,
        bgcolor: "#fafafa",
        borderRight: "1px solid #ddd",
        height: "calc(100vh - 64px)",
        overflowY: "auto",
        p: 2,
      }}
    >
      <Typography
        variant="h6"
        fontWeight="bold"
        gutterBottom
      >
        Investigation Panel
      </Typography>

      <Divider sx={{ mb: 2 }} />

      <HistoryPanel
        history={history}
        runQuery={runQuery}
        setCurrentQuestion={setCurrentQuestion}
    />


      <Divider sx={{ my: 3 }} />

      <BookmarkPanel
        bookmarks={bookmarks}
        runQuery={runQuery}
        setCurrentQuestion={setCurrentQuestion}
    />
    </Box>
  );
}