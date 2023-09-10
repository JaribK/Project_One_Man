<?php
                function deleteFile($filePath) {
                    if (file_exists($filePath)) {
                        if (unlink($filePath)) {
                            return true;
                        } else {
                            return false;
                        }
                    } else {
                        return false;
                    }
                }

                if (isset($_POST['delete'])) {
                    $filenameToDelete = $_POST['filename'];
                    $filePathToDelete = "uploads/" . $filenameToDelete;
                    if (deleteFile($filePathToDelete)) {
                        echo "<p>File '$filenameToDelete' has been deleted successfully.</p>";
                    } else {
                        echo "<p>Failed to delete the file '$filenameToDelete'.</p>";
                    }
                }
                header("Location: index.php");
?>