<?php
if (isset($_FILES["file"]) ) {
	$content_dir = "/tmp/";
	$src_filename = $_FILES["file"]["tmp_name"];
	$dst_filename = $_FILES["file"]["name"];
	$dst_filename = str_replace("/", "_", $dst_filename);
	print "src_filename".$src_filename."\n";
	print "dst_filename=".$dst_filename."\n";
	move_uploaded_file( $src_filename, $content_dir . '/' . $dst_filename);
}
?>
