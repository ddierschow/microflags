#!/usr/local/bin/python

import glob, os, sys
import pycountry

dat_file_tags = ['link', 'alias', 'division', 'note', 'infra', 'type']
div_keys = ('parent', 'name', 'code', 'filename', 'type')  # optional: note alias subs


def make_db(flagdat):
    dblist = [('', c[1], '', c[0].lower(), flagdat['type'].get(c[0], 'Organization')) for c in 
	      flagdat['division'].items()]
    dblist += [('', c.name, str(c.alpha2), str(c.alpha2.lower()), flagdat['type'].get(c.alpha2, 'Country')) for c in pycountry.countries]
    dblist += [(str(c.country_code), c.name, str(c.code), str(c.code.lower()), c.type.title()) for c in pycountry.subdivisions]
    dblist.sort()
    flagdat['subs'] = []
    flagdat['divs'] = []
    flagdat['orgs'] = []
    dbdict = {'': dict(zip(div_keys, [''] * len(div_keys)))}
    dbdict['']['subs'] = {}
    for cy in dblist:
	cy_d = dict(zip(div_keys, cy))
	if not cy_d['code']:
	    dbdict['']['subs'][cy_d['filename']] = cy_d
	    flagdat['orgs'].append(cy_d)
	elif cy_d['parent']:
	    dbdict[cy_d['parent']]['subs'][cy_d['code']] = cy_d
	    flagdat['subs'].append(cy_d)
	else:
	    cy_d['subs'] = dict()
	    dbdict[cy_d['code']] = cy_d
	    flagdat['divs'].append(cy_d)
    for cy in flagdat['note']:
	dbdict[cy]['note'] = flagdat['note'][cy]
    for cy in flagdat['alias']:
	if '-' in cy:
	    dbdict[cy[:2]]['subs'][cy]['alias'] = flagdat['alias'][cy]
	else:
	    dbdict[cy]['alias'] = flagdat['alias'][cy]


def write(out_file, outstr, endln='\n', encode='UTF8'):
    if encode:
	outstr = outstr.encode(encode)
    out_file.write(outstr + endln)


def format_array(array, keys=None):
    if isinstance(array, list):
	return ', '.join(['"%s"' % x.encode('UTF8') for x in array])
    if keys is None:
	keys = array.keys()
    return ', '.join(['"%s" => "%s"' % (x, array[x].encode('UTF8')) for x in keys if x in array])


def write_php_big_array(out_file, name, array, encode='UTF8'):
    write(out_file, '$%s = array();' % name, encode=encode)
    if isinstance(array, dict):
	for key in array:
	    write(out_file, '$%s["%s"] = %s;' % (name, key, array[key]), encode=encode)
    else:
	for ent in array:
	    write(out_file, '$%s[] = %s;' % (name, ent), encode=encode)
    write(out_file, "")


def make_div(cy):
    ret = format_array(cy, div_keys[1:] + ('note', 'alias'))
    return 'array(%s)' % ret


def make_subdiv(cy):
    ret = format_array(cy, div_keys + ('note', 'alias'))
    return 'array(%s)' % ret


def write_php_divs(fname, flagdat, verbose):
    out_file = open(fname, 'w')
    write(out_file, PHP_IMAGE_TOP)
    link_arr = {x: '"%s"' % flagdat['link'][x] for x in flagdat['link']}
    write_php_big_array(out_file, 'link', link_arr, encode=None)
    name_links = list(set([x['name'][0] if x['name'][0] <= 'Z' else 'other' for x in flagdat['divs'] + flagdat['orgs']]))
    code_links = list(set([x['code'][0] for x in flagdat['divs'] if x['code']]))
    name_links.sort()
    code_links.sort()
    write(out_file, "$%s = [%s];" % ('name_links', format_array(name_links)))
    write(out_file, "$%s = [%s];" % ('code_links', format_array(code_links)))
    div_arr = [make_div(x) for x in flagdat['divs'] + flagdat['orgs'] if x['parent'] == '']
    write_php_big_array(out_file, 'div', div_arr, encode=None)
    write(out_file, "?>")
    if verbose:
	count_div = count_fil = 0
	for x in flagdat['divs'] + flagdat['orgs']:
	    if x['code'] not in flagdat['alias']:
		count_div += 1
		count_fil += int(os.path.exists(x['filename'] + '.gif'))
	print 'Divisions %3d / %3d  (%3d%%)' % (count_fil, count_div, 100 * count_fil / count_div)


PHP_IMAGE_TOP = '''<?php
// File auto generated.  Do not change or check in.
'''


PHP_CY_IMAGE_TOP = '''include "flags.php";
include "divs.php";
'''

# here we have to define $parent and $subs.

PHP_CY_IMAGE_BOTTOM = '''subs_page($parent, $subs);
?>'''


def write_php_subdiv(cy, verbose):
    out_file = open(cy['code'].lower() + '.php', 'w')
    write(out_file, PHP_IMAGE_TOP)
    write(out_file, PHP_CY_IMAGE_TOP)
    write(out_file, '$parent = %s;' % make_div(cy), encode=None)
#    write(out_file, '$code2 = "%s";' % cy['code'])
#    if cy.get('note'):
#	write(out_file, '$note = "%s";' % cy['note'])
#    write(out_file, '$name = "%s";' % cy['name'])
#    write(out_file, '$fn = "%s";' % cy.get('alias', cy['code']).lower())
    sub_arr = [make_div(cy['subs'][x]) for x in cy['subs']]
    sub_arr.sort()
    write_php_big_array(out_file, 'subs', sub_arr, encode=None)
    write(out_file, PHP_CY_IMAGE_BOTTOM)
    if verbose:
	count_sub = count_fil = 0
	for x in cy['subs']:
	    if not 'alias' in cy['subs'][x]:
		count_sub += 1
		count_fil += int(os.path.exists(cy['subs'][x]['filename'] + '.gif'))
	print '%s %3d / %3d  (%3d%%)' % (cy['code'], count_fil, count_sub, 100 * count_fil / count_sub)


def write_php_subdivs(name, flagdat, verbose):
    out_file = open(name, 'w')
    write(out_file, PHP_IMAGE_TOP)
    sub_arr = [make_subdiv(x) for x in flagdat['subs']]
    write_php_big_array(out_file, 'subdiv', sub_arr, encode=None)
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


def is_websafe(img):
    img = img.convert('RGB')
    rgb = img_colors(img)
    if not rgb:
	return False
    for pxl in rgb.keys():
	if pxl[0] % 51 or pxl[1] % 51 or pxl[2] % 51:
	    return False
    return True


def img_colors(img):
    rgb = {}
    for x in range(0, img.size[0]):
	for y in range(0, img.size[1]):
	    pxl = img.getpixel((x,y))
	    if not rgb.has_key(pxl):
		rgb[pxl] = 0
	    rgb[pxl] = rgb[pxl] + 1
    return rgb


def show_counts(flagdat):
    import Image
    counts = {}
    not_ws = []
    too_large = []
    xs = set()
    ys = set()
    for ent in flagdat['divs'] + flagdat['subs'] + flagdat['orgs']:
	if ent.get('alias'):
	    continue
	fn = ent['filename'] + '.gif'
	if os.path.exists(fn):
	    img = Image.open(fn)
	    sz = img.size
	    xs.add(sz[0])
	    ys.add(sz[1])
	    counts.setdefault(sz[0], dict(t=0))
	    counts[sz[0]].setdefault(sz[1], 0)
	    counts[sz[0]][sz[1]] += 1
	    counts[sz[0]]['t'] += 1
	    if os.stat(fn).st_size > 300:
		too_large.append(fn)
	    if not is_websafe(img):
		not_ws.append(fn)
    print 'too large:', too_large
    print 'not websafe:', not_ws

    print "   |",
    for x in range(min(xs), max(xs) + 1):
	print "%3d" % x,
    print "|    t"
    print "-- +",
    for x in range(min(xs), max(xs) + 1):
	print "---",
    print '+ ----'
    for y in range(min(ys), max(ys) + 1):
	t = 0
	print "%2d |" % y,
	for x in range(min(xs), max(xs) + 1):
	    t += counts.get(x, {}).get(y, 0)
	    print "%3d" % counts.get(x, {}).get(y, 0),
	print "| %4d" % t
    print "-- +",
    for x in range(min(xs), max(xs) + 1):
	print "---",
    print '+ ----'
    print " t |",
    t = 0
    for x in range(min(xs), max(xs) + 1):
	t += counts.get(x, {}).get('t', 0)
	print "%3d" % counts.get(x, {}).get('t', 0),
    print "| %4d" % t


def show_orphans(flagdat):
    gifs = glob.glob('*.gif')
    for x in flagdat['divs'] + flagdat['subs'] + flagdat['orgs']:
	if (x['filename'] + '.gif') in gifs:
	    gifs.remove(x['filename'] + '.gif')
    for x in flagdat['infra']:
	if (flagdat['infra'][x]) in gifs:
	    gifs.remove(flagdat['infra'][x])
    print 'orphans:', gifs


if __name__ == '__main__':
    verbose = len(sys.argv) > 1 and sys.argv[1] == '-v'
    flagdat = get_data('flags.dat')
    make_db(flagdat)

    for cy in flagdat['divs']:
	if cy['subs']:
	    write_php_subdiv(cy, verbose)
    write_php_divs('divs.php', flagdat, verbose)
    write_php_subdivs('subdivs.php', flagdat, verbose)
    if verbose:
	show_orphans(flagdat)
	show_counts(flagdat)
