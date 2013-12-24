<?php
header('Content-Type: application/json');

if (isset($_GET['text']) and isset($_GET['index']) and isset($_GET['jsonp_callback'])) {
	echo $_GET['jsonp_callback'] .'({"keywords":'.exec('python content-affiliate-advertising.py "'.$_GET['text'].'" '.$_GET['index']).'})';
}
?>

