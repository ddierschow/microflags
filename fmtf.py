#!/usr/local/bin/python

import os, sys
import pycountry
import Image

dat_file_tags = ['link', 'alias', 'division', 'note']

def make_list(flagdat):
    dblist = [('', c[1][1], '', c[0], '', c[1][0]) for c in 
	      [(d, flagdat['division'][d].split('/')) for d in flagdat['division']]]
    dblist += [('', c.name, str(c.alpha2), str(c.alpha2.lower()), '', 'Country') for c in pycountry.countries]
    dblist += [(str(c.country_code), c.name, str(c.code), str(c.code.lower()), '', c.type.title()) for c in pycountry.subdivisions]
    dblist.sort()
    return dblist


def write(out_file, outstr, endln='\n', encode='UTF8'):
    if encode:
	outstr = outstr.encode(encode)
    out_file.write(outstr + endln)


def format_array(array):
    if isinstance(array, dict):
	return ', '.join(['"%s" => "%s"' % (x, array[x]) for x in array])
    return ', '.join(['"%s"' % x for x in array])


def write_php_big_array(out_file, name, array, encode='UTF8'):
    write(out_file, '$%s = array();' % name, encode=encode)
    if isinstance(array, dict):
	for key in array:
	    write(out_file, '$%s["%s"] = %s;' % (name, key, array[key]), encode=encode)
    else:
	for ent in array:
	    write(out_file, '$%s[] = %s;' % (name, ent), encode=encode)
    write(out_file, "")


def make_div(cy, alias):
    ret = '"%s", "%s", "%s", "%s"' % (cy[2], cy[1].encode('UTF8'), cy[3] + '.gif', cy[5].encode('UTF8'))
    if cy[2] in alias:
	ret += ', "%s"' % alias[cy[2]]
    return 'array(%s)' % ret


def write_php_divs(dblist, name, flagdat, verbose):
    out_file = open(name, 'w')
    write(out_file, PHP_IMAGE_TOP)
    link_arr = {x: '"%s"' % flagdat['link'][x] for x in flagdat['link']}
    write_php_big_array(out_file, 'link', link_arr, encode=None)
    name_links = list(set([x[1][0] if x[1][0] < 'Z' else 'other' for x in dblist if not x[0]]))
    code_links = list(set([x[2][0] for x in dblist if x[2]]))
    name_links.sort()
    code_links.sort()
    write(out_file, "$%s = [%s];" % ('name_links', format_array(name_links)))
    write(out_file, "$%s = [%s];" % ('code_links', format_array(code_links)))
    div_arr = [make_div(x, flagdat['alias']) for x in dblist if x[0] == '']
    write_php_big_array(out_file, 'div', div_arr, encode=None)
    write(out_file, "?>")
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

PHP_CY_IMAGE_BOTTOM = '''subs_page($code2, $name, $subs, $fn);
?>'''


def write_php_subdiv(dblist, code2, flagdat, verbose):
    out_file = open(code2.lower() + '.php', 'w')
    write(out_file, PHP_IMAGE_TOP)
    write(out_file, PHP_CY_IMAGE_TOP)
    write(out_file, '$code2 = "%s";' % code2)
    if code2 in flagdat['note']:
	write(out_file, '$note = "%s";' % flagdat['note'][code2])
    for x in dblist:
	if x[0] == '' and x[2] == code2:
	    write(out_file, '$name = "%s";' % x[1])
	    write(out_file, '$fn = "%s.gif";' % flagdat['alias'].get(x[2], x[2]).lower())
	    break
    sub_arr = [make_div(x, flagdat['alias']) for x in dblist if x[0] == code2]
    write_php_big_array(out_file, 'subs', sub_arr, encode=None)
    write(out_file, PHP_CY_IMAGE_BOTTOM)
    if verbose:
	count_sub = count_fil = 0
	for x in dblist:
	    if x[0] == code2 and x[2] not in flagdat['alias']:
		count_sub += 1
		count_fil += int(os.path.exists(x[3] + '.gif'))
	print code2, count_fil, '/', count_sub


def make_subdiv(cy, alias):
    ret = '"%s", "%s", "%s", "%s", "%s"' % (cy[0], cy[2], cy[1].encode('UTF8'), cy[3] + '.gif', cy[5].encode('UTF8'))
    if cy[2] in alias:
	ret += ', "%s"' % alias[cy[2]]
    return 'array(%s)' % ret


def write_php_subdivs(dblist, name, flagdat, verbose):
    out_file = open(name, 'w')
    write(out_file, PHP_IMAGE_TOP)
    sub_arr = [make_subdiv(x, flagdat['alias']) for x in dblist if x[0] != ""]
    write_php_big_array(out_file, 'subs', sub_arr, encode=None)
    write(out_file, "?>")


def get_data(fn):
    dat = {x: {} for x in dat_file_tags}
    for ln in open(fn):
	ln = ln.strip()
	if not ln or ln.startswith('#'):
	    continue
	ln = ln.split(' ', 2)
	dat[ln[0]][ln[1]] = ln[2]
    return dat


def show_counts(dblist, flagdat):
    counts = {}
    for ent in dblist:
	if ent[2] in flagdat['alias']:
	    continue
	fn = ent[3] + '.gif'
	if os.path.exists(fn):
	    sz = Image.open(fn).size
	    counts.setdefault(sz[0], dict())
	    counts[sz[0]].setdefault(sz[1], 0)
	    counts[sz[0]][sz[1]] += 1

    print "   |",
    for x in range(7, 33):
	print "%3d" % x,
    print
    print "-- +",
    for x in range(7, 33):
	print "---",
    print
    for y in range(9, 17):
	print "%2d |" % y,
	for x in range(7, 33):
	    print "%3d" % counts.get(x, {}).get(y, 0),
	print


if __name__ == '__main__':
    verbose = len(sys.argv) > 1 and sys.argv[1] == '-v'
    flagdat = get_data('flags.dat')
    dblist = make_list(flagdat)
    subs = []
    for ent in dblist:
	if ent[0] and ent[0] not in subs:
	    subs.append(ent[0])

    for arg in subs:
	write_php_subdiv(dblist, arg, flagdat, verbose)
    write_php_divs(dblist, 'divs.php', flagdat, verbose)
    write_php_subdivs(dblist, 'subdivs.php', flagdat, verbose)
    if verbose:
	show_counts(dblist, flagdat)
