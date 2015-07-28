#!/usr/local/bin/python

import pycountry

FOTW = 'http://www.crwflags.com/fotw/'


def make_list():
# {'alpha2': u'AF', 'alpha3': u'AFG', 'name': u'Afghanistan', '_element': <DOM Element: iso_3166_entry at 0x8057e25a8>, 'numeric': u'004', 'official_name': u'Islamic Republic of Afghanistan'}
# {'code': u'AD-07', 'type': u'Parish', '_element': <DOM Element: iso_3166_2_entry at 0x8065a2200>, 'country_code': u'AD', 'name': u'Andorra la Vella'}
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


def write_php_array(PHP, name, array, encode='UTF8'):
    write(PHP, '$%s = array();' % name, encode=encode)
    for ent in array:
	#fmt_ent = ', '.join([repr(x) for x in ent])
	write(PHP, '$%s[] = array(%s);' % (name, ent), encode=encode)


def make_div(cy, alias):
    ret = '"%s", "%s", "%s", "%s"' % (cy[2], cy[1].encode('UTF8'), cy[3] + '.gif', cy[5].encode('UTF8'))
    if cy[2] in alias:
	ret += ', "%s"' % alias[cy[2]]
    return ret


def write_php_divs(dblist, name, flagdat):
    #print name
    PHP = open(name, 'w')
    write(PHP, PHP_IMAGE_TOP)
    div_arr = [make_div(x, flagdat['alias']) for x in dblist if x[0] == '']
    write_php_array(PHP, 'div', div_arr, encode=None)
    write(PHP, "\n?>")


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


def make_subdiv(sd, alias):
    ret = '"%s", "%s", "%s", "%s"' % (sd[2], sd[1].encode('UTF8'), sd[3] + '.gif', sd[5].encode('UTF8'))
    if sd[2] in alias:
	ret += ', "%s"' % alias[sd[2]]
    return ret


def write_php_subdiv(dblist, code2, flagdat):
    name = code2.lower() + '.php'
    #print name
    PHP = open(name, 'w')
    write(PHP, PHP_IMAGE_TOP)
    write(PHP, PHP_CY_IMAGE_TOP)
    write(PHP, '$code2 = "%s";' % code2)
    for x in dblist:
	if x[0] == '' and x[2] == code2:
	    write(PHP, '$name = "%s";' % x[1])
	    write(PHP, '$fn = "%s.gif";' % flagdat['alias'].get(x[2], x[2]).lower())
	    break
    sub_arr = [make_div(x, flagdat['alias']) for x in dblist if x[0] == code2]
    write_php_array(PHP, 'subs', sub_arr, encode=None)
    write(PHP, PHP_CY_IMAGE_BOTTOM)



def write_php_subdivs(dblist, name, flagdat):
    #print name
    PHP = open(name, 'w')
    write(PHP, PHP_IMAGE_TOP)
    sub_arr = ['"%s", ' + make_div(x, flagdat['alias']) for x in dblist if x[0] != ""]
    write_php_array(PHP, 'subs', sub_arr, encode=None)
    write(PHP, "\n?>")


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
    flagdat = get_data('flags.dat')
    dblist = make_list()
    subs = []
    for ent in dblist:
	if ent[0] and ent[0] not in subs:
	    subs.append(ent[0])

    for arg in subs:
	write_php_subdiv(dblist, arg, flagdat)
    write_php_divs(dblist, 'divs.php', flagdat)
    write_php_subdivs(dblist, 'subdivs.php', flagdat)
