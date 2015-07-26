<?php
include "flags.php";
include "divs.php";

$name = "name";
$sortby = 1;

html_head();
top_links($name);
letter_links();
usort($div, "cmp");

$curr = '';
table_head();
foreach ($div as $arg) {
    if ($arg[$sortby][0] != $curr) {
	$curr = $arg[$sortby][0];
	table_banner($curr);
    }
    table_entry('', $arg);
}
table_tail();

html_tail();
?>
