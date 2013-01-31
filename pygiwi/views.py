from pyramid.view import view_config

from lib import renderers

import glob
import os
import os.path

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'pygiwi'}

#this view returns the wiki page content
@view_config(route_name="view_wiki", renderer="pygiwi:templates/wiki.mako")
def view_wiki(request):
    pagename = request.matchdict["page"]
    project = request.matchdict["project"]
    
    #construction of the wiki path
    wikiroot = request.registry.settings['wiki.root']  #from settings in .ini file.
    wikipath = os.path.join(wikiroot, project) #project name is the name of the git repository
    rootfilepath = os.path.join(wikipath, pagename) #we want one specific file into this directory
    
    files = glob.glob(rootfilepath+".*")  #list files with any extension
    f = files[0]   #we take the first matching file, undertermined results if two files only differs by extension

    ext = os.path.splitext(f)[1]
    content = open(f, "r").read()

    html = renderers[ext](content) #selection of the correct renderer from the file extension
    
    return {"wikis": ["un", "deux"], "content": html}