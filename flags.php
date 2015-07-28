<?php

$headers = ['Name', 'Code', 'Division Type', '&micro;Flag', 'Filename'];

function html_head() {
?><html>
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<title>Micro-Flags of the World</title>
<link rel="icon" href="favicon.ico" type="image/x-icon" />
<link rel="shortcut icon" href="favicon.ico" type="image/x-icon" />
<link rel="stylesheet" href="flags.css" type="text/css">
</head>
<body bgcolor="#FFFFFF">
<img src="logo.jpg" align="right">
<h1>&micro;Flags of the World</h1><p><hr><p>

The original intention of these flags were for use as in-line graphics with text.
These flags have been designed to be of a correct aspect ratio,
most with a height of 12 to 14 pixels, but some as little as 9 or as many as 16.
The widths mostly range from 13 to 28 pixels, with the smallest being 7 and the largest 33.
The sizes are less than 300 <u>bytes</u>!
They have also been designed with web-safe colors.
The image files have been named with the ISO3166 country codes for entities that have these codes assigned.
<p>

This page was designed and drawn by <a href="http://www.xocolatl.com/dean/">Dean Dierschow</a>.
<p><hr><p>

<?php
}


function top_links($this_page) {
?>
Links:

<img src="fotw.gif"> <a href="http://www.crwflags.com/fotw/flags/">FOTW Homepage</a>
| <img src="here.gif">
<?php if ($this_page == 'name') { ?>
List Countries by Name
<?php } else { ?>
<a href=".">List by Name</a>
<?php } ?>
| <img src="here.gif">
<?php if ($this_page == 'code') { ?>
List Countries by Code
<?php } else { ?>
<a href="code.php">List by Code</a>
<?php } ?>
<br>
<?php
}


function letter_links() {
?>
<a href="#A"><b>A</b></a>
 | <a href="#B"><b>B</b></a>
 | <a href="#C"><b>C</b></a>
 | <a href="#D"><b>D</b></a>
 | <a href="#E"><b>E</b></a>
 | <a href="#F"><b>F</b></a>
 | <a href="#G"><b>G</b></a>
 | <a href="#H"><b>H</b></a>
 | <a href="#I"><b>I</b></a>
 | <a href="#J"><b>J</b></a>
 | <a href="#K"><b>K</b></a>
 | <a href="#L"><b>L</b></a>
 | <a href="#M"><b>M</b></a>
 | <a href="#N"><b>N</b></a>
 | <a href="#O"><b>O</b></a>
 | <a href="#P"><b>P</b></a>
 | <a href="#Q"><b>Q</b></a>
 | <a href="#R"><b>R</b></a>
 | <a href="#S"><b>S</b></a>
 | <a href="#T"><b>T</b></a>
 | <a href="#U"><b>U</b></a>
 | <a href="#V"><b>V</b></a>
 | <a href="#W"><b>W</b></a>
 | <a href="#Y"><b>Y</b></a>
 | <a href="#Z"><b>Z</b></a>
 | <a href="#Å"><b>Å</b></a>
<p>
<?php
}

function table_head() {
    global $headers;
?>
<table>
  <tr class="header">
<?php
    foreach ($headers as $hdr)
        echo '<th>' . $hdr . '</th>';
?>
  </tr>
<?php
}

function table_banner($name) {
   echo ' <tr class="banner"><th colspan="6"><a name="' . $name . '">' . $name . "</a></th></tr>\n";
}

// code2, name, image name, entity type, link, alias
function table_entry($prnt, $arg) {
    echo '  <tr><td>';
    if ($prnt == '') {
	$lnk = '';
	if (array_key_exists(4, $arg))
	    $lnk = $arg[4];
	if ((strpos($lnk, 'http') === 0) || file_exists($lnk))
	    echo '<a href="' . $lnk . '">' . $arg[1] . '</a>';
	else
	    echo $arg[1];
    }
    else {
	echo '<img src="ball.gif" alt="o">';
	echo $arg[1];
    }
    echo '</td>';
    echo '<td>' . $arg[0] . '</td>';
    echo '<td>' . $arg[3] . '</td>';
    $fn = $arg[2];
    if (array_key_exists(5, $arg) and $arg[5])
	$fn = strtolower($arg[5]) . '.gif';
    if (file_exists($fn)) {
	echo '<td><center><a href="' . $fn . '"><img src="' . $fn . '" border=0></a></center></td>';
	echo '<td><code>' . $fn . '</code></td></tr>';
    }
    else {
	echo '<td>&nbsp;</td>';
	echo '<td>&nbsp;</td>';
    }
    echo "\n";
}

function table_tail() {
?>
</table>
<?php
}

function html_tail() {
?>
</body>
</html>
<?php
}

$sortby = 0;
function cmp($a, $b) {
    global $sortby;
    if ($a[$sortby] == $b[$sortby])
        return 0;
    return ($a[$sortby] < $b[$sortby]) ? -1 : 1;
}


function subs_page($code2, $name, $subs, $fn) {
    html_head();
    top_links($code2);

    table_head();
    table_entry('', [$code2, $name, $fn, 'Country']);
    foreach ($subs as $arg) {
	if (array_key_exists(4, $arg))
	    $arg[5] = $arg[4];
	$arg[4] = '';
	table_entry($code2, $arg);
    }
    table_tail();
}

html_tail();
?>
