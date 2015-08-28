<?php

$headers = ['Name', 'Code', 'Division Type', '&micro;Flag', 'Filename'];
$specials = ['name', 'code', 'all', 'check', 'sub'];
$row_n = 0;

function get_item($arr, $key, $default='') {
    return isset($arr[$key]) ? $arr[$key] : $default;
}

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
The widths mostly range from 14 to 28 pixels, with the smallest being 4 and the largest 32.
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
   echo ' <tr class="note"><td colspan="3">Note: <i>' . $note . '</i></td><td colspan="2">&nbsp;</td></tr>' . "\n";
}

function table_entry($prnt, $arg) {
    global $row_n;
    echo '  <tr class="row_' . $row_n . '"><td>';
    $row_n = ($row_n + 1) % 2;
    if ($prnt == '') {
	$lnk = '';
	if (array_key_exists('link', $arg))
	    $lnk = $arg['link'];
	if ((strpos($lnk, 'http') === 0) || file_exists($lnk))
	    echo '<a href="' . $lnk . '">' . $arg['name'] . '</a>';
	else
	    echo $arg['name'];
    }
    else {
	echo '<img src="ball.gif" alt="o">';
	echo $arg['name'];
    }
    echo '</td>';
    echo '<td>' . $arg['code'] . '</td>';
    echo '<td>' . $arg['type'] . '</td>';
    $fn = $arg['filename'] . '.gif';
    if (array_key_exists('alias', $arg) and $arg['alias'])
	$fn = strtolower($arg['alias']) . '.gif';
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

$cmp_sortby = 'name';
function cmp($a, $b) {
    global $cmp_sortby; // this one actually needs to be a global
    if ($a[$cmp_sortby] == $b[$cmp_sortby])
        return 0;
    return ($a[$cmp_sortby] < $b[$cmp_sortby]) ? -1 : 1;
}


// API
function subs_page($parent, $subs) {
    global $headers, $specials;
    global $link;
    global $note;
    html_head($link);
    top_links($parent['code'], $link, $parent['name'], $specials);

    table_head($headers);
    table_entry('', $parent);
    if (isset($parent['note']))
	table_note($parent['note']);
    foreach ($subs as $arg) {
	table_entry($parent['code'], $arg);
    }
    table_tail();
}

// API
function index_page($name, $sortby, $page_links, $sub='') {
    global $headers, $specials, $cmp_sortby;
    global $link;
    global $div, $subdiv;
    html_head($link);
    top_links($name, $link, $name, $specials);
    if (!$sub)
	letter_links($page_links);

    table_head($headers);
    $cmp_sortby = $sortby;
    usort($div, "cmp");
    $curr = '';
    foreach ($div as $arg) {
	if ($sub && ($arg['code'] != $sub))
	    continue;
	if ($arg[$sortby]) {
	    $code2 = $arg['code'];
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
		$arg['link'] = $link['FOTW'] . 'flags/' . strtolower($code2) . '.html';
		$arg['code'] = '<a href="tgm/?name=' . strtolower($code2) . '">' . $code2 . '</a>';
	    }
	    else if ($name == 'sub' && $code2) {
		$num_flags = $cnt_flags = 0;
		foreach ($subdiv as $sarg) {
		    if ($sarg['parent'] == $code2 && !array_key_exists('alias', $sarg)) {
			$num_flags += 1;
			$cnt_flags += (file_exists($sarg['filename'] . '.gif') ? 1 : 0);
		    }
		}
		$arg['link'] = $link['FOTW'] . 'flags/' . strtolower($code2) . '.html';
		$arg['code'] = '<a href="tgm/?name=' . strtolower($code2) . '">' . $code2 . '</a>';
		$arg['type'] = '<a href="?s=' . $code2 . '">' . $arg['type'] . '</a>';
		if ($num_flags > 0) {
		    $arg['type'] .= ' (' . $cnt_flags . '/' . $num_flags .  ')';
		}
	    }
	    else if ($name == 'check') {
		$arg['link'] = strtolower($code2) . '.php';
		$arg['type'] = '<img src="' . $link['FOTW'] . 'images/' . strtolower($code2[0]) . '/' . strtolower($code2) . '.gif">';
	    }
	    else {
		$arg['link'] = strtolower($code2) . '.php';
	    }
	    table_entry('', $arg);
	    if ($name == 'all' || ($code2 && $sub == $code2)) {
		if (isset($arg['note']))
		    table_note($arg['note']);
		foreach ($subdiv as $sarg) {
		    if ($sarg['parent'] == $code2) {
			$sarg['code'] = '<a href="tgm/?name=' . strtolower($sarg['code']) . '">' . $sarg['code'] . '</a>';
			table_entry($arg['code'], $sarg);
		    }
		}
	    }
	}
    }
    table_tail();

    html_tail();
}

?>
