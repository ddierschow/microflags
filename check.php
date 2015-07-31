<?php
include "flags.php";
include "divs.php";

$headers = ['Name', 'Code', 'Original Flag', '&micro;Flag', 'Filename'];
//$name = "check";
$sortby = 0;

index_page('check', $sortby, $code_links);
?>
