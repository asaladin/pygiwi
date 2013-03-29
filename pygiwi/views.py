from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

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

    
@view_config(route_name="wiki_project_home")
def wiki_project_home(request):
    """this view is called with urls like /wiki/project_name without page name. It should redirect to the 'home' page,
       ie Home"""
    project_name = request.matchdict['project']
    return HTTPFound(request.route_url('view_wiki', project=project_name, page='Home'))
    

@view_config(route_name='wiki_home2', renderer='pygiwi:templates/wiki_home.mako')    
@view_config(route_name='wiki_home', renderer='pygiwi:templates/wiki_home.mako')
def wiki_home(request):
    #create list of wikis:
    wikiroot = request.registry.settings['wiki.root']  #from settings in .ini file.
    wikis = os.listdir(wikiroot)
    
    return {'wikis': wikis}
    
    

@view_config(route_name="view_wiki", renderer="pygiwi:templates/wiki.mako")
def view_wiki(request):
    """this view returns the wiki page content
    """
    pagename = request.matchdict["page"]
    project = request.matchdict["project"]
    
    if pagename=='':
        return HTTPFound(request.route_url('view_wiki', project=project, page='Home'))
    
    content, ext = getPage(request, project, pagename)
    
    html = renderers[ext](unicode(content, 'utf-8'))
    
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
    
    