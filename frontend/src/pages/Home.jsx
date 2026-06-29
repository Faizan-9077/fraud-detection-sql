import { useState } from "react";

import { Box } from "@mui/material";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import MainContent from "../components/MainContent";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import api from "../services/api";

export default function Home() {

  const [sql, setSql] = useState("");
  const [results, setResults] = useState([]);
  const [rowCount, setRowCount] = useState(0);
  const [lastQuestion, setLastQuestion] = useState("");
  const [currentQuestion, setCurrentQuestion] = useState("");
  const [success, setSuccess] = useState(false);

  const [history, setHistory] = useState(() => {
    const saved = localStorage.getItem("queryHistory");
    return saved ? JSON.parse(saved) : [];
  });

  const [bookmarks, setBookmarks] = useState(() => {
    const saved = localStorage.getItem("bookmarks");
    return saved ? JSON.parse(saved) : [];
  });

  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "success",
});



  const addToHistory = (question) => {

    const historyItem = {
      question,
      timestamp: new Date().toLocaleString(),
    };

    const updatedHistory = [
      historyItem,
      ...history.filter(
        (item) => item.question !== question
      ),
    ].slice(0, 10);

    setHistory(updatedHistory);

    localStorage.setItem(
      "queryHistory",
      JSON.stringify(updatedHistory)
    );
  };



  const addBookmark = (question, sql) => {

    const bookmark = {
        question,
        sql,
        timestamp: new Date().toLocaleString(),
    };

    const updatedBookmarks = [
        bookmark,
        ...bookmarks.filter(
            item => item.question !== question
        ),
    ];

    setBookmarks(updatedBookmarks);

    localStorage.setItem(
        "bookmarks",
        JSON.stringify(updatedBookmarks)
    );
  };

  const removeBookmark = (question) => {
    const updatedBookmarks = bookmarks.filter(
      (item) => item.question !== question
    );

    setBookmarks(updatedBookmarks);
    localStorage.setItem("bookmarks", JSON.stringify(updatedBookmarks));
  };

    const showSnackbar = (
      message,
        severity = "success"
    ) => {

        setSnackbar({
            open: true,
            message,
            severity,
        });

    };

  const toggleBookmark = (question, sql) => {
    if (!question.trim()) return;

    const isBookmarked = bookmarks.some(
      (item) => item.question === question
    );

    if (isBookmarked) {
      removeBookmark(question);
      showSnackbar("Investigation removed from bookmarks.", "info");
    } else {
      addBookmark(question, sql);
      showSnackbar("Investigation bookmarked!", "success");
    }
  };

    const handleCloseSnackbar = () => {

        setSnackbar(prev => ({
            ...prev,
            open: false,
        }));

    };

    const runQuery = async (question) => {
      if (!question.trim()) return;

      setCurrentQuestion(question);

      try {
          const response = await api.post("/query", { question });

          setSql(response.data.sql);
          setResults(response.data.results);
          setRowCount(response.data.row_count);
          setLastQuestion(question);
          setSuccess(true);

          addToHistory(question);
      } catch (error) {
          setSuccess(false);

          showSnackbar(
              error.response?.data?.error || "Query failed.",
              "error"
          );
      }
  };


    const exportCSV = () => {

      if (!results.length) return;

      const headers = Object.keys(results[0]);

      const csv = [

          headers.join(","),

          ...results.map(row =>
              headers.map(h => `"${row[h]}"`).join(",")
          ),

      ].join("\n");

      const blob = new Blob(
          [csv],
          {
              type: "text/csv",
          }
      );

      const url = URL.createObjectURL(blob);

      const a = document.createElement("a");

      a.href = url;

      a.download = "aml_results.csv";

      a.click();

      URL.revokeObjectURL(url);

      showSnackbar(
          "CSV exported successfully!"
      );

  };


const exportPDF = () => {

    if (!results.length) return;

    const doc = new jsPDF({
        orientation: "landscape",
    });

    doc.setFont("helvetica", "bold");
    doc.setFontSize(18);
    doc.text("AML Investigation Report", 14, 24);

    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);

    doc.text(
        `Generated: ${new Date().toLocaleString()}`,
        14,
        34,
        { maxWidth: 260 }
    );

    doc.text(
        `Question: ${lastQuestion}`,
        14,
        44,
        { maxWidth: 260 }
    );

    doc.text(
        `Rows Returned: ${rowCount}`,
        14,
        56,
        { maxWidth: 260 }
    );

    doc.setFont("helvetica", "bold");
    doc.text(
        "Generated SQL:",
        14,
        68,
        { maxWidth: 260 }
    );

    doc.setFont("helvetica", "normal");
    doc.setFontSize(9);
    doc.text(
        sql,
        14,
        76,
        { maxWidth: 260 }
    );

    const formatValue = (value) => {
      if (value === null || value === undefined) return "";
      if (typeof value === "number") {
        return Number.isInteger(value)
          ? value.toLocaleString()
          : value.toLocaleString(undefined, {
              minimumFractionDigits: 0,
              maximumFractionDigits: 2,
            });
      }
      return String(value);
    };

    const headers = [Object.keys(results[0])];

    const body = results.map((row) =>
      Object.values(row).map(formatValue)
    );

    autoTable(doc, {
      head: headers,
      body,
      startY: 92,
      margin: { left: 14, right: 14 },
      tableWidth: "auto",
      styles: {
        fontSize: 8,
        cellPadding: 3,
        overflow: "linebreak",
        cellWidth: "wrap",
        halign: "left",
        valign: "middle",
      },
      headStyles: {
        fillColor: [41, 128, 185],
        textColor: 255,
        fontStyle: "bold",
      },
    });

    const finalY =
        doc.lastAutoTable.finalY + 15;

    doc.setFontSize(10);

    doc.text(
        "Generated by Fraud Detection & Compliance Reporting Dashboard",
        14,
        finalY
    );

    doc.text(
        "Accenture Internship Project",
        14,
        finalY + 8
    );

    doc.save("AML_Investigation_Report.pdf");

    showSnackbar(
        "SAR PDF exported successfully!"
    );

};




  return (
    <>
      <Navbar />

      <Box
        sx={{
          display: "flex",
          height: "calc(100vh - 64px)",
        }}
      >
        <Sidebar
            history={history}
            bookmarks={bookmarks}
            runQuery={runQuery}
            setCurrentQuestion={setCurrentQuestion}
        />

        <MainContent
            sql={sql}
            results={results}
            rowCount={rowCount}
            lastQuestion={lastQuestion}
            success={success}
            currentQuestion={currentQuestion}
            setCurrentQuestion={setCurrentQuestion}
            runQuery={runQuery}
            toggleBookmark={toggleBookmark}
            isBookmarked={bookmarks.some(
              (item) => item.question === lastQuestion
            )}
            showSnackbar={showSnackbar}
            exportCSV={exportCSV}
            exportPDF={exportPDF}
        />
      </Box>


    <Snackbar
        open={snackbar.open}
        autoHideDuration={3000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{
            vertical: "bottom",
            horizontal: "right",
        }}
    >
        <Alert
            severity={snackbar.severity}
            variant="filled"
            onClose={handleCloseSnackbar}
        >
            {snackbar.message}
        </Alert>
    </Snackbar>
    </>
  );
}