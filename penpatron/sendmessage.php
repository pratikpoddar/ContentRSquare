<?php
	$file = 'messages.txt';
	// Open the file to get existing content
	$current = file_get_contents($file);
	// Append a new person to the file
	$current .= "!!!!!!!!!!!!!!!\n";
	foreach ( $_POST as $key => $value )
	{
        	$current .= "----\n";
		$current .= $key."\n";
		$current .= $value."\n";
	}
	$current .= "!!!!!!!!!!!!!!\n";
	// Write the contents back to the file
	file_put_contents($file, $current);
?>
