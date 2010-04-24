<?php

// only one file allowed
echo "==POST==<br/>\n";
foreach(array_keys($_POST) as $key) {
    echo $key." = ".$_POST[$key]."<br/>\n";
}
echo "==/POST==<br/>\n";
echo "==GET==<br/>\n";
foreach(array_keys($_GET) as $key) {
    echo $key." = ".$_GET[$key]."<br/>\n";
}
echo "==/GET==<br/>\n";
print_r($_FILES);
echo "==FILES==<br/>\n";
foreach(array_keys($_FILES) as $key) {
    echo "==FILE key ".$key."==<br/>\n";
	$content_dir = "/tmp/";
    echo "==debug==<br/>\n";
    print_r($_FILES[$key]);
    echo "==/debug==<br/>\n";
	$src_filename = $_FILES[$key]["tmp_name"];
	$dst_filename = $_FILES[$key]["name"];
	$dst_filename = str_replace("/", "_", $dst_filename);
	print "src_filename".$src_filename."<br/>\n";
	print "dst_filename=".$dst_filename."<br/>\n";
	move_uploaded_file( $src_filename, $content_dir . '/' . $dst_filename);
}
echo "==/FILE==<br/>\n";
?>
