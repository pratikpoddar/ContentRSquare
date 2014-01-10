<?php
header('Content-Type: application/json');

if (isset($_GET['text']) and isset($_GET['index']) and isset($_GET['jsonp_callback'])) {
	 $newld = "/var/www/ContentRSquare";
         $saved = getenv("PATH");
	 if ($saved) { $newld .= ":$saved"; }
	 putenv("PATH=$newld");
         $saved = getenv("PYTHONPATH");
         if ($saved) { $newld .= ":$saved"; }
         putenv("PYTHONPATH=$newld");
	echo $_GET['jsonp_callback'].'({"keywords":'.exec('python content-affiliate-advertising.py "'.str_replace('"',"",str_replace("'","",$_GET['text'])).'" "'.$_GET['index'].'"').'})';
}
?>
