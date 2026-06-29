import { Box } from "@mui/material";

import QueryInput from "./QueryInput";
import SummaryCards from "./SummaryCards";
import SQLViewer from "./SQLViewer";
import ResultsTable from "./ResultsTable";
import ExportButtons from "./ExportButtons";

export default function MainContent(props) {
  return (
    <Box
      sx={{
        flex: 1,
        p: 3,
        overflow: "auto",
      }}
    >
      <QueryInput
          question={props.currentQuestion}
          setQuestion={props.setCurrentQuestion}
          runQuery={props.runQuery}
      />

      <SummaryCards
        rowCount={props.rowCount}
        success={props.success}
        question={props.lastQuestion}
      />

      <ExportButtons

      results={props.results}

      exportCSV={props.exportCSV}

      exportPDF={props.exportPDF}

      />

      <SQLViewer 
        toggleBookmark={props.toggleBookmark}
        isBookmarked={props.isBookmarked}
        lastQuestion={props.lastQuestion}
        sql={props.sql} 
        showSnackbar={props.showSnackbar}
        />

      <ResultsTable
        results={props.results}
        rowCount={props.rowCount}
      />
    </Box>
  );
}