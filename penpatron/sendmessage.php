<?php
	$file = 'message'.time().'.txt';
	$handle = fopen($file, 'w');
	$current = "!!!!!!!!!!!!!!!\n";
	$current .= time()."\n";
	foreach ( $_POST as $key => $value )
	{
        	$current .= "----\n";
		$current .= $key."\n";
		$current .= $value."\n";
	}
	$current .= "!!!!!!!!!!!!!!\n";
	fwrite($handle, $current);
?>
