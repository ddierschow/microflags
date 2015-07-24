#!/usr/local/bin/python

import os, random, sys
import Image
import cmdline

SWITCHES = ""
OPTIONS = ""

width = 20
HTML = sys.stdout

def Write(outstr, endln='\n'):
    HTML.write(outstr + endln)


if __name__ == '__main__':

    HTML = file('big.html', 'w')
    switch, files = cmdline.CommandLine(SWITCHES, OPTIONS)

    sdict = {}
    ilist = []
    for arg in files:
	img = Image.open(arg)
	img = img.convert('RGB')
	if img.size[0] > 33 or img.size[1] > 16:
	    continue

	if not sdict.has_key(img.size):
	    sdict[img.size] = []
	sdict[img.size].append(arg)
	ilist.append(arg)

    '''
    kl = sdict.keys()
    kl.sort()

    sl = []
    for i in range(0,17):
    	sl.append([0]*34)
    for k in kl:
	sl[k[1]][k[0]] = len(sdict[k])

    print "    ",
    for x in range(11, 34):
	    print "%3d" % x,
    print
    for y in range(9, 17):
	print "%2d :" % y,
	for x in range(11, 34):
	    print "%3d" % sl[y][x],
	print
    '''

    c = y = 0
    Write("<html><body><center><table>")
    while ilist:
	Write("<tr>")
	for x in range(0, width):
	    if not ilist:
		break
	    if x == (width / 2 - 2) and y == (width / 2 - 2):
		Write('<td rowspan=5 colspan=4><center><img src="logo.gif" align=middle></center></td>')
	    elif x >= (width / 2 - 2) and x < (width / 2 + 2) and y >= (width / 2 - 2) and y < (width / 2 + 3):
		pass
	    else:
		f = random.choice(ilist)
		Write('<td><center><img src="%s" align=middle alt="%s"></center></td>' % (f, f))
		ilist.remove(f)
		c = c + 1
	y = y + 1
	Write("</tr>")
    Write("</table></center></body></html>")
    print c, "usable flags found."


#logo.gif: GIF image data, version 89a, 98 x 69
