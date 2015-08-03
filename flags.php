<?php

$headers = ['Name', 'Code', 'Division Type', '&micro;Flag', 'Filename'];
$specials = ['name', 'code', 'all', 'check'];

function html_head($link) {
?><!DOCTYPE html>
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<title>Micro-Flags of the World</title>
<link rel="icon" href="favicon.ico" type="image/x-icon" />
<link rel="shortcut icon" href="favicon.ico" type="image/x-icon" />
<link rel="stylesheet" href="flags.css" type="text/css">
</head>
<body>
<img src="logo.jpg" align="right">
<h1>&micro;Flags of the World</h1><p><hr><p>

The original intention of these flags were for use as in-line graphics with text.
These flags have been designed to be of a correct aspect ratio,
most with a height of 12 to 15 pixels, but some as few as 9 or as many as 16.
The widths mostly range from 14 to 28 pixels, with the smallest being 7 and the largest 32.
The sizes are less than 300 <u>bytes</u>!
They have also been designed with web-safe colors.
The image files have been named with the ISO3166 country codes for entities that have these codes assigned.
<p>

This page was designed and drawn by <a href="<?php echo $link['AUTHOR']; ?>">Dean Dierschow</a>.
<p><hr><p>

<?php
}


function top_links($this_page, $link, $name, $specials) {
?>
Links:

<img src="fotw.gif"> <a href="<?php echo $link['FOTW']; ?>">FOTW Homepage</a>
| <img src="iso.gif"> <a href="<?php echo $link['ISO']; ?>">ISO 3166 Maintenance Agency</a>
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
<?php if (!in_array($this_page, $specials)) { ?>
<img src="fotw.gif"> <a href="<?php echo $link['FOTW'] . 'flags/' . strtolower($this_page) . '.html'; ?>">FOTW Page for <?php echo $name; ?></a>
<?php } ?>
<br>
<?php
}


function letter_links($links) {
    foreach ($links as $ind => $val) {
	if ($ind)
	    echo '| ';
	echo '<a href="#' . $val . '"><b>' . ucfirst($val) . "</b></a>\n";
    }
}

function table_head($headers) {
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

function table_banner($link, $name) {
   echo ' <tr class="banner"><th colspan="5"><a name="' . $link . '">' . $name . "</a></th></tr>\n";
}

function table_note($note) {
   echo ' <tr><td colspan="3">Note: <i>' . $note . '</i></td><td colspan="2">&nbsp;</td></tr>' . "\n";
}

// arg = code2, name, image name, entity type, link, alias
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
</html><?php
}

$sortby = 0;
function cmp($a, $b) {
    global $sortby; // this one actually needs to be a global
    if ($a[$sortby] == $b[$sortby])
        return 0;
    return ($a[$sortby] < $b[$sortby]) ? -1 : 1;
}


function subs_page($code2, $name, $subs, $fn) {
    global $headers, $specials;
    global $link;
    global $note;
    html_head($link);
    top_links($code2, $link, $name, $specials);

    table_head($headers);
    table_entry('', [$code2, $name, $fn, 'Country']);
    if (isset($note))
	table_note($note);
    foreach ($subs as $arg) {
	if (array_key_exists(4, $arg))
	    $arg[5] = $arg[4];
	$arg[4] = '';
	table_entry($code2, $arg);
    }
    table_tail();
}

function index_page($name, $sortby, $page_links) {
    global $headers, $specials;
    global $link;
    global $div, $subs;
    html_head($link);
    top_links($name, $link, $name, $specials);
    letter_links($page_links);

    table_head($headers);
    usort($div, "cmp");
    $curr = '';
    foreach ($div as $arg) {
	if ($arg[$sortby]) {
	    $code2 = $arg[0];
	    if ($arg[$sortby][0] != $curr) {
		$new = $curr;
		if ($curr <= 'Z' && $curr != 'Other') {
		    if ($arg[$sortby][0] > 'Z')
			$new = 'other';
		    else
			$new = $arg[$sortby][0];
		}
		if ($new != $curr) {
		    $curr = $new;
		    table_banner($curr, ucfirst($curr));
		}
	    }
	    if ($name == 'all') {
		$arg[4] = $link['FOTW'] . 'flags/' . strtolower($code2) . '.html';
		$arg[0] = '<a href="tgm/?name=' . strtolower($code2) . '">' . $code2 . '</a>';
	    }
	    else if ($name == 'check') {
		$arg[4] = strtolower($code2) . '.php';
		$arg[3] = '<img src="' . $link['FOTW'] . 'images/' . strtolower($code2[0]) . '/' . strtolower($code2) . '.gif">';
	    }
	    else {
		if (array_key_exists(4, $arg))
		    $arg[5] = $arg[4];
		$arg[4] = strtolower($code2) . '.php';
	    }
	    table_entry('', $arg);
	    if ($name == 'all') {
		foreach ($subs as $sarg) {
		    if ($sarg[0] == $code2) {
			$sarg[1] = '<a href="tgm/?name=' . strtolower($sarg[1]) . '">' . $sarg[1] . '</a>';
			table_entry($arg[2], array_slice($sarg, 1));
		    }
		}
	    }
	}
    }
    table_tail();

    html_tail();
}

?>
