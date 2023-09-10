<?php 
    header("Content-type: text/css; charset:UFT-8");
?>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500&family=Itim&display=swap');
body {
    font-family: 'Inter', sans-serif;
    font-family: 'Itim', cursive;
    margin: 0;
}

.header{
    display: flex;
    justify-content: center;
    width: 100%;
}

.header p {
    font-size: xx-large;
}

.body {
    margin: 30px;
}

.input{
    display:flex;
    justify-content: center;
    align-items: start;
    width:100%;
}

input.submit-button{
    font-family: 'Inter', sans-serif;
    font-family: 'Itim', cursive;
    border: none;
    background: rgb(200, 200, 200);
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
}

input.submit-button:hover{
    font-family: 'Inter', sans-serif;
    font-family: 'Itim', cursive;
    background: rgb(75, 75, 255);
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    cursor: pointer;
}

input[type='file']::file-selector-button{
    font-family: 'Inter', sans-serif;
    font-family: 'Itim', cursive;
    border: none;
    background: rgb(200, 200, 200);
    color: white;
    border-radius: 4px 0px 0px 4px;
    padding: 10px 20px;
}

input[type='file']::file-selector-button:hover{
    font-family: 'Inter', sans-serif;
    font-family: 'Itim', cursive;
    background: rgb(75, 75, 255);
    color: white;
    border-radius: 4px 0px 0px 4px;
    padding: 10px 20px;
    cursor: pointer;
}

input[type='file']::choose-file-button{
    font-family: 'Inter', sans-serif;
    font-family: 'Itim', cursive;
    border: none;
}

input[type='file']{
    font-family: 'Inter', sans-serif;
    font-family: 'Itim', cursive;
    border: solid rgb(100, 100, 100) 1px;
    border-radius: 10px;
}

.order-files {
    padding: 5px;
}

table{
    width: 100%;
    border-collapse: collapse;
}

th{
    border-bottom: 3px solid black;
    width: 25%;
    padding: 8px;
    text-align: left;
  }

td{
    border-bottom: 1px solid black;
    width: 25%;
    padding: 8px;
    text-align: left;
  }

select {
    font-family: 'Inter', sans-serif;
    font-family: 'Itim', cursive;
    border: none;
    background: rgb(200, 200, 200);
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
}

a:link {
    text-decoration: none;
    color: black;
}

#download{
    font-family: 'Inter', sans-serif;
    font-family: 'Itim', cursive;
    background: rgb(100, 255, 100);
    border: rgb(75, 190, 75) solid 1px;
    padding: 10px 20px;
    border-radius: 7px;
}
#download:hover{
    font-family: 'Inter', sans-serif;
    font-family: 'Itim', cursive;
    background: rgb(75, 190, 75);
    border: solid 1px green;
    cursor: pointer;
    padding: 10px 20px;
    border-radius: 7px;
}

#delete {
    font-family: 'Inter', sans-serif;
    font-family: 'Itim', cursive;
    background: rgb(253, 100, 100);
    padding: 10px 20px;
    border: rgb(185, 75, 75) solid 1px;
    border-radius: 7px;
}
#delete:hover {
    font-family: 'Inter', sans-serif;
    font-family: 'Itim', cursive;
    background: rgb(185, 75, 75);
    padding: 10px 20px;
    border: solid 1px red;
    cursor: pointer;
    border-radius: 7px;
}