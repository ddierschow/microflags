<?php
include "flags.php";
include "divs.php";
include "subdivs.php";

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
    $arg[4] = 'http://www.crwflags.com/fotw/flags/' . strtolower($arg[0]) . '.html';
    table_entry('', $arg);

    foreach ($subs as $sarg) {
	if ($sarg[0] == $arg[0])
	    table_entry($arg[2], array_slice($sarg, 1));
    }

}
table_tail();

html_tail();
?>
