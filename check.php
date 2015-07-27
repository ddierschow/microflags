<?php
include "flags.php";
include "divs.php";

$headers = ['Name', 'Code', 'Original Flag', '&micro;Flag', 'Filename'];
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
	$arg[4] = strtolower($arg[0]) . '.php';
	$arg[3] = '<img src="http://www.crwflags.com/fotw/images/' . strtolower($arg[0][0]) . '/' . strtolower($arg[0]) . '.gif">';
	table_entry('', $arg);
    }
}
table_tail();

html_tail();
?>
