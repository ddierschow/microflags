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


def write_php_divs(dblist, name):
    print name
    PHP = open(name, 'w')
    write(PHP, '<?php\n')
    div_arr = ['"%s", "%s", "%s", "%s"' % (x[2], x[1].encode('UTF8'), x[3] + '.gif', x[5]) for x in dblist if x[0] == '']
    write_php_array(PHP, 'div', div_arr, encode=None)
    write(PHP, "\n?>")


PHP_IMAGE_TOP = '''<?php
include "flags.php";
include "divs.php";
'''

# here we have to define $code2, $name, and $subs.

PHP_CY_IMAGE_BOTTOM = '''
subs_page($code2, $name, $subs);
?>'''


def write_php_subdiv(dblist, code2):
    name = code2.lower() + '.php'
    print name
    PHP = open(name, 'w')
    write(PHP, PHP_IMAGE_TOP)
    write(PHP, '$code2 = "%s";' % code2)
    for x in dblist:
	if x[0] == '' and x[2] == code2:
	    write(PHP, '$name = "%s";' % x[1])
	    break
    sub_arr = ['"%s", "%s", "%s", "%s"' % (x[2], x[1].encode('UTF8'), x[3] + '.gif', x[5].encode('UTF8')) for x in dblist if x[0] == code2]
    write_php_array(PHP, 'subs', sub_arr, encode=None)
    write(PHP, PHP_CY_IMAGE_BOTTOM)


if __name__ == '__main__':
    dblist = make_list()
    subs = []
    for ent in dblist:
	if ent[0] and ent[0] not in subs:
	    subs.append(ent[0])

    for arg in subs:
	write_php_subdiv(dblist, arg)
    write_php_divs(dblist, 'divs.php')
