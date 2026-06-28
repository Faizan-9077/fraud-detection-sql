import {
    Typography,
    List,
    ListItemButton,
    ListItemText,
} from "@mui/material";

export default function HistoryPanel({
    history,
}) {

    return (
        <>
            <Typography
                variant="subtitle1"
                fontWeight="bold"
                gutterBottom
            >
                Query History
            </Typography>

            <List dense>

                {history.length === 0 ? (

                    <ListItemText
                        primary="No history yet"
                        secondary="Run a query"
                    />

                ) : (

                    history.map((item, index) => (

                        <ListItemButton key={index}>
                          <ListItemText
                              primary={item.question}
                              secondary={item.timestamp}
                          />
                      </ListItemButton>

                    ))

                )}

            </List>
        </>
    );
}