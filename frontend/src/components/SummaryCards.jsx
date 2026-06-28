import {
  Grid,
  Card,
  CardContent,
  Typography,
} from "@mui/material";

import TableRowsIcon from "@mui/icons-material/TableRows";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import QuestionAnswerIcon from "@mui/icons-material/QuestionAnswer";

export default function SummaryCards({
  rowCount,
  question,
  success,
}) {
  const cards = [
    {
      title: "Rows Returned",
      value: rowCount,
      icon: <TableRowsIcon color="primary" sx={{ fontSize: 40 }} />,
    },
    {
      title: "Status",
      value: success ? "Success" : "Waiting",
      icon: (
        <CheckCircleIcon
          color={success ? "success" : "disabled"}
          sx={{ fontSize: 40 }}
        />
      ),
    },
    {
      title: "Last Question",
      value: question || "-",
      icon: (
        <QuestionAnswerIcon
          color="secondary"
          sx={{ fontSize: 40 }}
        />
      ),
    },
  ];

  return (
    <Grid container spacing={3} sx={{ mb: 3 }}>
      {cards.map((card) => (
        <Grid item xs={12} md={4} key={card.title}>
          <Card elevation={3}>
            <CardContent>
              {card.icon}

              <Typography
                variant="subtitle2"
                color="text.secondary"
                sx={{ mt: 1 }}
              >
                {card.title}
              </Typography>

              <Typography
                variant="h6"
                sx={{
                  fontWeight: 700,
                  wordBreak: "break-word",
                }}
              >
                {card.value}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
}