<html>
<head>
<style>
body {background-color: #FFFFFF;}
img {display: block; margin-left: auto; margin-right: auto;}
</style>
</head>
<body>
<center><table>
<?php

$width = 20;
$height = 48;
$xm = 2;
$xp = 2 + ($width % 2);
$ym = 2;
$yp = 3;

function get_images() {
    $ignores = ["logo.gif", "ball.gif", "iso.gif", "fotw.gif"];
    $imgs = array();
    if ($dh = opendir(getcwd())) {
        while (($fn = readdir($dh)) !== false) {
	    $sizes = getimagesize($fn);
	    if (substr($fn, -4) == '.gif' && ($sizes[0] <= 32) && ($sizes[1] <= 16) && !in_array($fn, $ignores))
		$imgs[] = $fn;
        }
        closedir($dh);
    }
    return $imgs;
}

$imgs = get_images();
shuffle($imgs);
//sort($imgs);
$y = 0;
while (count($imgs) >= $width) {
    echo "<tr>\n";
    for ($x = 0; $imgs && ($x < $width); $x = $x + 1) {
	if ($x == floor($width / 2 - $xm) && $y >= floor($width / 2 - $ym) && $y < floor($width / 2 + $yp)) {
	    if ($y == floor($width / 2 - $ym))
		echo '<td rowspan="' . ($ym + $yp) . '" colspan="' . ($xm + $xp) . '"><center><img src="logo.gif" align=middle></center></td>' . "\n";
	    $x = $x + $xp + 1;
	}
	else {
	    $f = array_pop($imgs);
	    echo '<td><img src="' . $f . '" alt="' . $f . '"></td>' . "\n";
	}
    }
    $y = $y + 1;
    echo "</tr>\n";
    if ($y >= $height)
	break;
}

?>
</table></center>

</body>
</html>
