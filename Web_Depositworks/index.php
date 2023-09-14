<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.php">
    <link href='https://unpkg.com/css.gg@2.0.0/icons/css/software-upload.css' rel='stylesheet'>
    <title>Upload Files by Kingo</title>
</head>
<body>
    <div class="header">
        <div class="title">
            <p>งานอะไรนักหนาวะ?</p>
        </div>
    </div>
    <div class="body">
        <div class="input">
            <form method="POST" enctype="multipart/form-data" action="upload.php">
                <input class="choose-file-button" id="upfiles" type="file" name="file" required>
                <input class="submit-button" type="submit" value="อัปโหลดไฟล์">
            </form>
        </div>
        <br>
        <div class="table">
            <table>
                <thead>
                    <tr>
                        <th>Files</th>
                        <th>Types</th>
                        <th>Size</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <?php

                function getExtension($str){
                    $i = explode('.', $str);
                    return strtolower(end($i));
                }
    
                function formatBytes($bytes, $precision = 2) {
                    $units = array('B', 'KB', 'MB', 'GB', 'TB');
                    $bytes = max($bytes, 0);
                    $pow = floor(($bytes ? log($bytes) : 0) / log(1024));
                    $pow = min($pow, count($units) - 1);
                    $bytes /= pow(1024, $pow);

                    return round($bytes, $precision) . ' ' . $units[$pow];
                }

                $files = scandir("uploads");
                
                for ($a = 2; $a < count($files); $a++) {
                    $filePath = "uploads/" . $files[$a];
                    $fileSize = filesize($filePath);
                    $fileSizeFormatted = formatBytes($fileSize);
                    ?>
                        <table class="order-files">
                            <tr>
                                <td><?php echo substr($files[$a], 0, strrpos($files[$a], ".")); ?></td>
                                <td><?php echo getExtension($files[$a]) ?></td>
                                <td id = 2><?php echo $fileSizeFormatted ?></td>
                                <td>
                                    <form action="delete.php" method="POST">
                                        <button type="submit0" id="download"><a download="<?php echo $files[$a] ?>" href="uploads/<?php echo $files[$a] ?>">ดาวน์โหลดไฟล์</a></button>
                                        <input type="hidden" name="filename" value="<?php echo $files[$a]; ?>">
                                        <button type="submit" name="delete" id="delete">ลบไฟล์</button>
                                        <button type="submit2" id="rename">เปลี่ยนชื่อไฟล์</button>
                                    </form>
                                </td>
                            </tr>
                        </table>
                    <?php
                }
                ?>
            </table>
        </div>
    </div>
</body>
</html>