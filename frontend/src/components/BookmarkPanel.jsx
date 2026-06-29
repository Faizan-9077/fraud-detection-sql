import {

Typography,

List,

ListItemButton,

ListItemText,

} from "@mui/material";

export default function BookmarkPanel({

bookmarks,
runQuery,
setCurrentQuestion,

}) {

return (

<>

<Typography

variant="subtitle1"

fontWeight="bold"

gutterBottom

>

Bookmarks

</Typography>

<List dense>

{bookmarks.length===0 ? (

<ListItemText

primary="No bookmarks"

secondary="Save investigations later"

/>

) : (

bookmarks.map((item,index)=>(

<ListItemButton
    key={index}
    onClick={() => {
        setCurrentQuestion(item.question);
        runQuery(item.question);
    }}
>

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