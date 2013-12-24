<?php
header('Content-Type: application/json');
//$text = $_POST['text'];
//$options = $_POST['options'];
//$tracker = $_POST['tracker'];

//echo "[{'keyword': 'Columbia Business School', 'link': 'http://www.cseblog.com'}]";
echo $_GET['jsonp_callback'] .'({"keywords":'.exec('python content-affiliate-advertising.py "'.$_GET['text'].'" '.$_GET['options']['index']).'})';
//echo $_GET['jsonp_callback'] .'({"keywords":[{"keyword": "Columbia Business School", "link": "http://www.cseblog.com/checking"}, {"keyword": "IBM", "link": "http://www.pratikpoddar.com"}]})';
?>

