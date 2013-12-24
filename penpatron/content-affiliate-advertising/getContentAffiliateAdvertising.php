<?php
header('Content-Type: application/json');
//$text = $_POST['text'];
//$options = $_POST['options'];
//$tracker = $_POST['tracker'];
if (strpos($_SERVER['HTTP_REFERER'], "secretpratikpoddar")==FALSE) {
	echo $_GET['jsonp_callback']."()";
}

else {

	//echo "[{'keyword': 'Columbia Business School', 'link': 'http://www.cseblog.com'}]";
	echo $_GET['jsonp_callback'] .'({"keywords":'.exec('python content-affiliate-advertising.py "'.$_GET['text'].'" '.$_GET['index']).'})';
	//echo $_GET['jsonp_callback'] .'({"keywords":[{"keyword": "Columbia Business School", "link": "http://www.cseblog.com/checking"}, {"keyword": "IBM", "link": "http://www.pratikpoddar.com"}]})';
}
?>

