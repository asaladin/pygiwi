from pyramid.view import view_config

from lib import renderers

import glob
import os
import os.path


def getPage(request, project, pagename):
    """
    this function takes the request object (for configuration values in registry), the project name and the pagename and  
    returns the corresponding file content
    """
    
    #construction of the wiki path
    wikiroot = request.registry.settings['wiki.root']  #from settings in .ini file.
    wikipath = os.path.join(wikiroot, project) #project name is the name of the git repository
    rootfilepath = os.path.join(wikipath, pagename) #we want one specific file into this directory
    
    files = glob.glob(rootfilepath+".*")  #list files with any extension
    f = files[0]   #we take the first matching file, undertermined results if two files only differs by extension

    ext = os.path.splitext(f)[1]
    content = open(f, "r").read()
    
    return content, ext
    
    
@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'pygiwi'}
    

@view_config(route_name="view_wiki", renderer="pygiwi:templates/wiki.mako")
def view_wiki(request):
    """this view returns the wiki page content
    """
    pagename = request.matchdict["page"]
    project = request.matchdict["project"]
    
    content, ext = getPage(request, project, pagename)
    html = renderers[ext](content)
    
    #create list of wikis:
    wikiroot = request.registry.settings['wiki.root']  #from settings in .ini file.
    wikis = os.listdir(wikiroot)
        
    return {"wikis": wikis, "content": html}
    
@view_config(route_name = "edit", renderer = "pygiwi:editpage.mako")
def edit_wiki(request):
    """this view displays the raw content of the edited file for editing
    """    
    project = request.matchdict["project"]
    page = request.matchdict["page"]
    
    content,ext = getPage(request, project, page)
    
    return {"project": project, "content": content}
    
    