#!/usr/local/bin/python

import os, sys
import pycountry

FOTW = 'http://www.crwflags.com/fotw/'


def make_list():
    dblist = [
	('', 'European Union', '', 'eu', '', 'Union'),
	('', 'International Committee of the Red Cross', '', 'icrc', '', 'Organization'),
	('', 'International Committee of the Red Cross (Red Crescent) ', '', 'icrct', '', 'Organization'),
	('', 'International Committee of the Red Cross (Red Crystal) ', '', 'icrcl', '', 'Organization'),
	('', 'International Olympic Committee ', '', 'ioc', '', 'Organization'),
	('', 'North Atlantic Treaty Organization ', '', 'nato', '', 'Organization'),
	('', 'United Nations ', '', 'un', '', 'Organization'),
    ]
    dblist += [('', c.name, str(c.alpha2), str(c.alpha2.lower()), '', 'Country') for c in pycountry.countries]
    dblist += [(str(c.country_code), c.name, str(c.code), str(c.code.lower()), '', c.type) for c in pycountry.subdivisions]
    dblist.sort()
    return dblist


def write(out_file, outstr, endln='\n', encode='UTF8'):
    if encode:
	outstr = outstr.encode(encode)
    out_file.write(outstr + endln)


def write_php_array(out_file, name, array, encode='UTF8'):
    write(out_file, '$%s = array();' % name, encode=encode)
    for ent in array:
	#fmt_ent = ', '.join([repr(x) for x in ent])
	write(out_file, '$%s[] = array(%s);' % (name, ent), encode=encode)


def make_div(cy, alias):
    ret = '"%s", "%s", "%s", "%s"' % (cy[2], cy[1].encode('UTF8'), cy[3] + '.gif', cy[5].encode('UTF8'))
    if cy[2] in alias:
	ret += ', "%s"' % alias[cy[2]]
    return ret


def write_php_divs(dblist, name, flagdat, verbose):
    #print name
    out_file = open(name, 'w')
    write(out_file, PHP_IMAGE_TOP)
    div_arr = [make_div(x, flagdat['alias']) for x in dblist if x[0] == '']
    write_php_array(out_file, 'div', div_arr, encode=None)
    write(out_file, "\n?>")
    if verbose:
	count_div = count_fil = 0
	for x in dblist:
	    if x[0] == '' and x[2] not in flagdat['alias']:
		count_div += 1
		count_fil += int(os.path.exists(x[3] + '.gif'))
	print 'Divisions', count_fil, '/', count_div


PHP_IMAGE_TOP = '''<?php
// File auto generated.  Do not change or check in.
'''


PHP_CY_IMAGE_TOP = '''include "flags.php";
include "divs.php";
'''

# here we have to define $code2, $name, $subs, and $fn.

PHP_CY_IMAGE_BOTTOM = '''
subs_page($code2, $name, $subs, $fn);
?>'''


def write_php_subdiv(dblist, code2, flagdat, verbose):
    name = code2.lower() + '.php'
    #print name
    out_file = open(name, 'w')
    write(out_file, PHP_IMAGE_TOP)
    write(out_file, PHP_CY_IMAGE_TOP)
    write(out_file, '$code2 = "%s";' % code2)
    for x in dblist:
	if x[0] == '' and x[2] == code2:
	    write(out_file, '$name = "%s";' % x[1])
	    write(out_file, '$fn = "%s.gif";' % flagdat['alias'].get(x[2], x[2]).lower())
	    break
    sub_arr = [make_div(x, flagdat['alias']) for x in dblist if x[0] == code2]
    write_php_array(out_file, 'subs', sub_arr, encode=None)
    write(out_file, PHP_CY_IMAGE_BOTTOM)
    if verbose:
	count_sub = count_fil = 0
	for x in dblist:
	    if x[0] == code2 and x[2] not in flagdat['alias']:
		count_sub += 1
		count_fil += int(os.path.exists(x[3] + '.gif'))
	print code2, count_fil, '/', count_sub



def write_php_subdivs(dblist, name, flagdat, verbose):
    #print name
    out_file = open(name, 'w')
    write(out_file, PHP_IMAGE_TOP)
    sub_arr = ['"%s", ' + make_div(x, flagdat['alias']) for x in dblist if x[0] != ""]
    write_php_array(out_file, 'subs', sub_arr, encode=None)
    write(out_file, "\n?>")


def get_data(fn):
    dat = {}
    for ln in open(fn):
	ln = ln.strip()
	if not ln or ln.startswith('#'):
	    continue
	ln = ln.split(' ', 2)
	dat.setdefault(ln[0], dict())
	dat[ln[0]][ln[1]] = ln[2]
    return dat


if __name__ == '__main__':
    verbose = len(sys.argv) > 1 and sys.argv[1] == '-v'
    flagdat = get_data('flags.dat')
    dblist = make_list()
    subs = []
    for ent in dblist:
	if ent[0] and ent[0] not in subs:
	    subs.append(ent[0])

    for arg in subs:
	write_php_subdiv(dblist, arg, flagdat, verbose)
    write_php_divs(dblist, 'divs.php', flagdat, verbose)
    write_php_subdivs(dblist, 'subdivs.php', flagdat, verbose)
