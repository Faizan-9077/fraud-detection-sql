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
        setSql={props.setSql}
        setResults={props.setResults}
        setRowCount={props.setRowCount}
        setLastQuestion={props.setLastQuestion}
        setSuccess={props.setSuccess}
        addToHistory={props.addToHistory}
        showSnackbar={props.showSnackbar}

    />

      <SummaryCards
        rowCount={props.rowCount}
        success={props.success}
        lastQuestion={props.lastQuestion}
      />

      <ExportButtons

      results={props.results}

      exportCSV={props.exportCSV}

      exportPDF={props.exportPDF}

      />

      <SQLViewer 
        addBookmark={props.addBookmark}
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