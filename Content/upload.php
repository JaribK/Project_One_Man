<?php 
$my_folder = "./uploads/";

if (move_uploaded_file($_FILES['file']['tmp_name'], $my_folder . $_FILES['file']['name'])) {
    echo 'Received file' . $_FILES['file']['name'] . ' with size ' . $_FILES['file']['size'];
} else {
    echo 'Upload failed!';

    var_dump($_FILES['file']['error']);
}
header("Location: index.php");
?>