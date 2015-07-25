<?php
include "flags.php";
include "divs.php";

$name = "code";
$sortby = 0;

html_head();
top_links($name);
letter_links();
usort($div, "cmp");

$curr = '';
table_head();
foreach ($div as $arg) {
    if ($arg[0]) {
	if ($arg[$sortby][0] != $curr) {
	    $curr = $arg[$sortby][0];
	    table_banner($curr);
	}
	table_entry('', $arg);
    }
}
table_tail();

html_tail();
?>
