import {
  Paper,
  Typography,
  Divider,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  TableContainer,
  Chip,
} from "@mui/material";

export default function ResultsTable({ results, rowCount }) {

  if (!results || results.length === 0) {
    return (
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6">
          Query Results (0)
        </Typography>

        <Divider sx={{ my: 2 }} />

        <Typography color="text.secondary">
          No results to display.
        </Typography>
      </Paper>
    );
  }

  const columns = Object.keys(results[0]);

  return (
    <Paper elevation={3} sx={{ p: 3 }}>

      <Typography
        variant="h6"
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 2,
        }}
      >
        Query Results

        <Chip
          label={`${rowCount} Rows`}
          color="primary"
          size="small"
        />
      </Typography>

      <Divider sx={{ my: 2 }} />

      <TableContainer sx={{ maxHeight: 520 }}>

        <Table stickyHeader>

          <TableHead>

            <TableRow>

              {columns.map((column) => (

                <TableCell
                  key={column}
                  sx={{
                    fontWeight: "bold",
                    backgroundColor: "#f5f5f5",
                  }}
                >
                  {column}
                </TableCell>

              ))}

            </TableRow>

          </TableHead>

          <TableBody>

            {results.map((row, index) => (

              <TableRow key={index} hover>

                {columns.map((column) => (

                  <TableCell key={column}>

                    {String(row[column])}

                  </TableCell>

                ))}

              </TableRow>

            ))}

          </TableBody>

        </Table>

      </TableContainer>

    </Paper>
  );
}