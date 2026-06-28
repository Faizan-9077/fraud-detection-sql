import { Button, Stack } from "@mui/material";

import DownloadIcon from "@mui/icons-material/Download";
import PictureAsPdfIcon from "@mui/icons-material/PictureAsPdf";

export default function ExportButtons({
    results,
    exportCSV,
    exportPDF,
}) {

    return (

        <Stack
            direction="row"
            spacing={2}
            sx={{ mb: 2 }}
        >

            <Button
                variant="contained"
                startIcon={<DownloadIcon />}
                onClick={exportCSV}
                disabled={!results.length}
            >
                Export CSV
            </Button>

            <Button
                variant="contained"
                color="secondary"
                startIcon={<PictureAsPdfIcon />}
                onClick={exportPDF}
                disabled={!results.length}
            >
                Export SAR PDF
            </Button>

        </Stack>

    );

}