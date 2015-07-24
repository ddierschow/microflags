#!/usr/local/bin/python

import glob, os, re, sys, time
import pycountry

#----------------------------------
# Exposed controls - should be args perhaps.

DAT_FILE = 'flags.dat'
FOTW = 'http://www.crwflags.com/fotw/'
MAIN_COLOR = 0x0000FF

#----------------------------------
# Helpful data

indent_html = ['', '<img src="ball.gif" alt="o">']
cols = ['Country', 'Code', '&micro;Flag', 'Filename']
HEADER_COLOR = 0x999999
BODY_COLOR = 0xCCCCCC
HTML = sys.stdout

all_gifs = glob.glob('*.gif')

#----------------------------------
# Output functions

def Write(HTML, outstr, endln='\n'):
    outstr = outstr.encode('UTF8')
    HTML.write(outstr + endln)


def WriteTableHeader(HTML):
    Write(HTML, '<p>\n\n<table bgcolor="#%x">' % BODY_COLOR)


def WriteTableFooter(HTML):
    Write(HTML, '</table>')


def WriteFlagHeader(HTML):
    th = '<th bgcolor="#%x">' % (HEADER_COLOR | MAIN_COLOR)
    hdr = reduce(lambda x,y: x+th+y+'</th>', cols, '')
    Write(HTML, '  <tr>'+hdr+'</tr>')


def WriteFlag(HTML, name, code2, fname, indent=0, alt=None, nlink=True, clink=False, sbig=False):
    if code2 == '*':
	WriteText(HTML, fname, name)
	return

    refp = MakeFOTW(fname)
    if alt:
	refp = MakeFOTW(alt)

    # cell 1
    outstr = '  <td>' + indent_html[indent]
    if nlink and os.path.exists(code2.lower() + '.html'):
	outstr = outstr + '<a href="%s.html">%s</a>' % (code2.lower(), name)
    else:
	outstr = outstr + name
    # cell 2
    outstr = outstr + '</td><td>'
    outstr = outstr + code2
    outstr = outstr + '</td>'
    # cell 3 and 4
    if fname == '-':
	outstr = outstr + '<td colspan=2>(no flag)'
    elif os.path.exists(fname + '.gif'):
	href = fname + '.gif'
	if alt != None:
	    href = refp
	outstr = outstr + '<td><center><a href="%s"><img src="%s.gif" border=0></a></center></td>' % (href, fname)
	if fname + '.gif' in all_gifs:
	    all_gifs.remove(fname + '.gif')
	if sbig:
	    outstr = outstr + '<td><img src="%s">' % refp
	else:
	    outstr = outstr + '<td><code>%s.gif</code>' % (fname)
    else:
	outstr = outstr + '<td><center>&nbsp;</center></td><td>&nbsp;'
    outstr = outstr + '</td>'
    Write(HTML, '  <tr>' + outstr + '</tr>')


def WriteText(HTML, name, text):
    if name:
	Write(HTML, ' <tr><th bgcolor="#%x" colspan=5><a name="%s"><font size=+1>%s</font></a></th></tr>' % (BODY_COLOR | MAIN_COLOR, name, text))
    else:
	Write(HTML, ' <tr><th bgcolor="#%x" colspan=5>%s</font></th></tr>' % (BODY_COLOR | MAIN_COLOR, text))


def WritePageHeader(HTML, page):
    Write(HTML, '''<html>
<head>
<title>Micro-Flags of the World</title>
<link rel="icon" href="http://www.bamca.org/flags/favicon.ico" type="image/x-icon" />
<link rel="shortcut icon" href="http://www.bamca.org/flags/favicon.ico" type="image/x-icon" />
</head>
<body bgcolor="#FFFFFF">
<img src="logo.jpg" align="right">
<h1>&micro;Flags of the World</h1><p><hr><p>

The original intention of these flags were for use as in-line graphics with text.
These flags have been designed to be of a correct aspect ratio,
most with a height of 12 to 14 pixels, but some as little as 9 or as many as 16.
The widths mostly range from 12 to 30 pixels, and the sizes are less than a thousand <u>bytes</u> (most are under 300!).
They have also been designed with web-safe colors.
The image files have been named with the ISO3166 country codes for entities that have these codes assigned.
<p>

This page was designed and drawn by <a href="http://www.xocolatl.com/dean/">Dean Dierschow</a>.
<p><hr><p>

Links:
''')
# | <img src="iso.gif"> <a href="http://www.iso.org/iso/en/prods-services/iso3166ma/index.html">Information on the ISO3166 List</a>

    Write(HTML, '<img src="fotw.gif"> <a href="%s">FOTW Homepage</a>' % FOTW)
    if page == Alpha:
	Write(HTML, '| <img src="here.gif"> List by Name')
    else:
	Write(HTML, '| <img src="here.gif"> <a href="../flags">List by Name</a>')
    if page == Code:
	Write(HTML, '| <img src="here.gif"> List by Code')
    else:
	Write(HTML, '| <img src="here.gif"> <a href="code.html">List by Code</a>')
    Write(HTML, '<br>\n')


def WritePageFooter(HTML):
    #Write(HTML, time.strftime('\n<font size=-1><i>Last updated %A, %d %B %Y at %I:%M:%S %p %Z.</i></font>', time.localtime(time.time())))

    Write(HTML, '</body>\n</html>')


def WriteJumpList(HTML, dictJumps):
    listJumps = dictJumps.keys()
    listJumps.sort(lambda x,y: cmp(dictJumps[x], dictJumps[y]))
    for jump in listJumps:
	if jump != listJumps[0]:
	    Write(HTML, ' | ', '')
	Write(HTML, '<a href="#%s"><b>%s</b></a>' % (jump,dictJumps[jump]))

#----------------------------------
# Data functions

def GetArg(llist, arg, value=""):
    nvalue = None
    if len(llist) > arg:
        nvalue = llist[arg].strip()
    if nvalue:
	value = nvalue
    return value


def MakeList():

# {'alpha2': u'AF', 'alpha3': u'AFG', 'name': u'Afghanistan', '_element': <DOM Element: iso_3166_entry at 0x8057e25a8>, 'numeric': u'004', 'official_name': u'Islamic Republic of Afghanistan'}
# {'code': u'AD-07', 'type': u'Parish', '_element': <DOM Element: iso_3166_2_entry at 0x8065a2200>, 'country_code': u'AD', 'name': u'Andorra la Vella'}
    dblist = [
	('', 'European Union', '', 'eu', ''),
	('', 'International Committee of the Red Cross', '', 'icrc', ''),
	('', 'International Committee of the Red Cross (Red Crescent) ', '', 'icrct', ''),
	('', 'International Committee of the Red Cross (Red Crystal) ', '', 'icrcl', ''),
	('', 'International Olympic Committee ', '', 'ioc', ''),
	('', 'North Atlantic Treaty Organization ', '', 'nato', ''),
	('', 'United Nations ', '', 'un', ''),
    ]
    dblist += [('', c.name, str(c.alpha2), str(c.alpha2.lower()), '') for c in pycountry.countries]
    dblist += [(str(c.country_code), c.name, str(c.code), str(c.code.lower()), '') for c in pycountry.subdivisions]
    dblist.sort()
    return dblist


def MakeFOTW(fname):
    # actually should be url join but this will do for now
    return os.path.join(FOTW, 'images', fname[0], fname + '.gif')

#----------------------------------
# Page renderers

def Alpha(HTML, dblist, pname):
    letter = ''
    letterdict = {}
    for llist in dblist:
	if not llist[0]:
	    letter = llist[1][0].upper()
	    if not letter in letterdict.keys():
		letterdict[letter] = letter
    WriteJumpList(HTML, letterdict)
    letter = ""

    WriteTableHeader(HTML)
    WriteFlagHeader(HTML)

    for llist in dblist:
    	prnt, name, code2, fname, alt = llist
    	if prnt:
    	    continue
    	if letter != name[0].upper():
	    letter = name[0].upper()
    	    WriteText(HTML, letter, letter)
	WriteFlag(HTML, name, code2, fname)

    WriteTableFooter(HTML)


def Code(HTML, dblist, pname):
    letterdict = {}
    noncodes = '&-*'
    for llist in dblist:
	if llist[2] and llist[2][0] not in noncodes:
	    letter = llist[2][0].upper()
	    if not letter in letterdict.keys():
		letterdict[letter] = letter
    WriteJumpList(HTML, letterdict)
    letter = ""

    dblist.sort(lambda x,y: cmp(x[2], y[2]))
    WriteTableHeader(HTML)
    WriteFlagHeader(HTML)

    for llist in dblist:
    	prnt, name, code2, fname, alt = llist
    	if prnt or not code2 or code2[0] == '&':
    	    continue
    	if letter != code2[0].upper():
	    letter = code2[0].upper()
    	    WriteText(HTML, letter, letter)
	WriteFlag(HTML, name, code2, fname)

    WriteTableFooter(HTML)


def All(HTML, dblist, pname):
    dict = {}
    for llist in dblist:
	if llist[0] and not dict.has_key(llist[0]):
	    dict[llist[0]] = llist[0]
    WriteJumpList(HTML, dict)

    WriteTableHeader(HTML)
    WriteFlagHeader(HTML)

    letter = ''
    for llist in dblist:
    	prnt, name, code2, fname, alt = llist
    	if prnt and letter != prnt:
	    letter = prnt
    	    WriteText(HTML, prnt, prnt)
	if code2.startswith('-'):
	    WriteFlag(HTML, name, prnt.upper() + code2, fname, alt=alt, clink=True)
	else:
	    WriteFlag(HTML, name, code2, fname, alt=alt, clink=True)

    WriteTableFooter(HTML)


def Check(HTML, dblist, pname):
    WriteTableHeader(HTML)
    WriteFlagHeader(HTML)

    for llist in dblist:
    	prnt, name, code2, fname, alt = llist
	if code2.startswith('-'):
	    WriteFlag(HTML, name, prnt.upper() + code2, fname, alt=alt, clink=True, sbig=True)
	else:
	    WriteFlag(HTML, name, code2, fname, alt=alt, clink=True, sbig=True)

    WriteTableFooter(HTML)


def Subdiv(HTML, dblist, pname):
    WriteTableHeader(HTML)
    WriteFlagHeader(HTML)

    for llist in dblist:
    	prnt, name, code2, fname, alt = llist
    	if code2.lower() == pname.lower():
    	    WriteFlag(HTML, name, code2, fname, nlink=False)
    	elif prnt.lower() == pname.lower():
	    if code2[0] == '-':
		WriteFlag(HTML, name, pname.upper() + code2, fname, indent=1, nlink=False)
	    else:
		WriteFlag(HTML, name, code2, fname, indent=1, nlink=False)

    WriteTableFooter(HTML)


objs = {'all.html' : All, 'index.html' : Alpha, 'code.html' : Code, 'check.html' : Check}


def WriteHTML(dblist, arg):
    HTML = open(arg, 'w')
    Order = objs.get(arg, Subdiv)
    WritePageHeader(HTML, Order)
    Order(HTML, dblist, arg[:-5])
    WritePageFooter(HTML)

#----------------------------------
# main

if __name__ == '__main__':
    if len(sys.argv) > 1:
	files = sys.argv[1:]
    else:
	files = []
	for subdiv in pycountry.subdivisions:
	    subfile = subdiv.country_code.lower() + '.html'
	    if subfile not in files:
		files.append(subfile)
	files += objs.keys()
    dblist = MakeList()
    for arg in files:
	if arg == DAT_FILE or arg[-4:] == '.gif':
	    continue
	print arg
	WriteHTML(dblist, arg)
