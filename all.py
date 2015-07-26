#!/usr/local/bin/python

import glob, os, re, sys, time
import pycountry

#----------------------------------
# Exposed controls - should be args perhaps.

FOTW = 'http://www.crwflags.com/fotw/'
MAIN_COLOR = 0x0000FF

#----------------------------------
# Helpful data

indent_html = ['', '<img src="ball.gif" alt="o">']
cols = ['Country', 'Code', '&micro;Flag', 'Filename']
HEADER_COLOR = 0x999999
BODY_COLOR = 0xCCCCCC

all_gifs = glob.glob('*.gif')

#----------------------------------
# Output functions

def write(out_file, outstr, endln='\n', encode='UTF8'):
    if encode:
	outstr = outstr.encode(encode)
    out_file.write(outstr + endln)


def write_table_header(out_file):
    write(out_file, '<p>\n\n<table bgcolor="#%x">' % BODY_COLOR)


def write_table_footer(out_file):
    write(out_file, '</table>')


def write_flag_header(out_file):
    th = '<th bgcolor="#%x">' % (HEADER_COLOR | MAIN_COLOR)
    hdr = reduce(lambda x,y: x+th+y+'</th>', cols, '')
    write(out_file, '  <tr>'+hdr+'</tr>')


def write_flag(out_file, name, code2, fname, indent=0, alt=None, nlink=True, clink=False, sbig=False):
    if code2 == '*':
	write_text(out_file, fname, name)
	return

    refp = make_fotw(fname)
    if alt:
	refp = make_fotw(alt)

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
    write(out_file, '  <tr>' + outstr + '</tr>')


def write_text(out_file, name, text):
    if name:
	write(out_file, ' <tr><th bgcolor="#%x" colspan=5><a name="%s"><font size=+1>%s</font></a></th></tr>' % (BODY_COLOR | MAIN_COLOR, name, text))
    else:
	write(out_file, ' <tr><th bgcolor="#%x" colspan=5>%s</font></th></tr>' % (BODY_COLOR | MAIN_COLOR, text))


def write_page_header(out_file, page):
    write(out_file, '''<html>
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

    write(out_file, '<img src="fotw.gif"> <a href="%s">FOTW Homepage</a>' % FOTW)
    write(out_file, '| <img src="here.gif"> <a href="../flags">List by Name</a>')
    write(out_file, '| <img src="here.gif"> <a href="code.html">List by Code</a>')
    write(out_file, '<br>\n')


def write_page_footer(out_file):
    #write(out_file, time.strftime('\n<font size=-1><i>Last updated %A, %d %B %Y at %I:%M:%S %p %Z.</i></font>', time.localtime(time.time())))

    write(out_file, '</body>\n</html>')

#----------------------------------
# Data functions

def make_list():

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


def make_fotw(fname):
    # actually should be url join but this will do for now
    return os.path.join(FOTW, 'images', fname[0], fname + '.gif')

#----------------------------------
# Page renderers

def render_all(out_file, dblist, pname):
    dict = {}
    for llist in dblist:
	if llist[0] and not dict.has_key(llist[0]):
	    dict[llist[0]] = llist[0]

    write_table_header(out_file)
    write_flag_header(out_file)

    letter = ''
    for llist in dblist:
    	prnt, name, code2, fname, alt = llist
    	if prnt and letter != prnt:
	    letter = prnt
    	    write_text(out_file, prnt, prnt)
	if code2.startswith('-'):
	    write_flag(out_file, name, prnt.upper() + code2, fname, alt=alt, clink=True)
	else:
	    write_flag(out_file, name, code2, fname, alt=alt, clink=True)

    write_table_footer(out_file)


def render_check(out_file, dblist, pname):
    write_table_header(out_file)
    write_flag_header(out_file)

    for llist in dblist:
    	prnt, name, code2, fname, alt = llist
	if code2.startswith('-'):
	    write_flag(out_file, name, prnt.upper() + code2, fname, alt=alt, clink=True, sbig=True)
	else:
	    write_flag(out_file, name, code2, fname, alt=alt, clink=True, sbig=True)

    write_table_footer(out_file)


def write_html(dblist, arg):
    print arg
    out_file = open(arg, 'w')
    render_type = objs[arg]
    write_page_header(out_file, render_type)
    render_type(out_file, dblist, arg[:-5])
    write_page_footer(out_file)

objs = {'all.html' : render_all, 'check.html' : render_check}

#----------------------------------
# main

if __name__ == '__main__':
    files = objs.keys()
    dblist = make_list()
    for arg in files:
	write_html(dblist, arg)
