#!/usr/bin/env python

import unicodedata
import re
import os
import conf

BUILD = '_build'

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens. Thanks Django
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)

def converter(adir='./%s/html' % BUILD):
    for f in os.listdir(adir):
        f = os.path.join(adir, f)
        if os.path.isfile(f) and f.endswith('.html'):
            for x in ('static','sources'):
                os.system('sed "s/_%s/sphinx_%s/g" "%s" > "%s.tmp"' % (x,x,f,f))
                os.system('mv "%s.tmp" "%s"' % (f,f))
        elif os.path.isdir(f):
            converter(f)
            
converter()

os.system('mv ./%s/html/_static ./%s/html/sphinx_static' % (BUILD, BUILD))
os.system('mv ./%s/html/_sources ./%s/html/sphinx_sources' % (BUILD, BUILD))

slug = slugify(conf.project)
os.system('mv ./%s/html ../../sphinxdoc.github.com/%s' % (BUILD, slug))
os.chdir('../../sphinxdoc.github.com')
os.system('git add %s' % slug)
os.system('git commit %s -m "added %s"' % (slug, conf.project))
os.system('git push origin master')
