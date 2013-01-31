from pyramid.view import view_config

from lib import renderers

import glob
import os

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'pygiwi'}


@view_config(route_name="view_wiki", renderer="pygiwi:templates/wiki.mako")
def view_wiki(request):
    pagename = request.matchdict["page"]
    project = request.matchdict["project"]
    
    files = glob.glob("/home/saladin/Src/Web/Pyramid/testwiki/%s.*"%pagename)
    print "files:", files
    f = files[0]   #we take the first matching file, undertermined results if two files only differs by extension
    ext = os.path.splitext(f)[1]
    content = open(f, "r").read()

    html = renderers[ext](content)
    
    
    return {"wikis": ["un", "deux"], "content": html}