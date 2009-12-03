#!/usr/bin/env python

import unicodedata
import re
import os
import conf


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens. Thanks Django
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)

def converter(adir='./build/html'):
    for f in os.listdir(adir):
        f = os.path.join(adir, f)
        if os.path.isfile(f) and f.endswith('.html'):
            for x in ('static','sources'):
                os.system('sed "s/_%s/sphinx_%s/g" "%s" > "%s.tmp"' % (x,x,f,f))
                os.system('mv "%s.tmp" "%s"' % (f,f))
        elif os.path.isdir(f):
            converter(f)
            
converter()

os.system('mv ./build/html/_static ./build/html/sphinx_static')
os.system('mv ./build/html/_sources ./build/html/sphinx_sources')

slug = slugify(conf.project)
os.system('mv ./build/html ../sphinxdoc.github.com/%s' % slug)
os.chdir('../sphinxdoc.github.com')
os.system('git add %s' % slug)
os.system('git commit %s -m "added %s"' % (slug, conf.project))
os.system('git push origin master')
