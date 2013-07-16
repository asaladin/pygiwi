from pyramid.view import view_config
from pyramid.view import notfound_view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid

from dulwich.repo import Repo

from lib import renderers, formats, get_user_infos
from lib import mkdir_p, custom_route_path

import glob
import os
import os.path

import logging
log = logging.getLogger(__name__)


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
    
   

@view_config(route_name="view_wiki", renderer="pygiwi:templates/wiki.mako", permission="view")
def view_wiki(request):
    """this view returns the wiki page content
    """
    pagename = request.matchdict["page"]
    project = request.matchdict["project"]
    
    if pagename=='':
        return HTTPFound(request.route_url('view_wiki', project=project, page='Home'))
    
    try:
        content, ext = getPage(request, project, pagename)
    except:
        mydict = dict(pagename = pagename, url="/createwiki/%s/%s"%(project, pagename) )
        raise HTTPNotFound()
    
    html = renderers[ext](unicode(content, 'utf-8'))
    
    #create list of wikis:
    wikiroot = request.registry.settings['wiki.root']  #from settings in .ini file.
    wikis = os.listdir(wikiroot)
    
    edit_url = custom_route_path(request, "edit", project=project, page=pagename)
        
    return {"wikis": wikis, "content": html, "format": formats[ext], "edit_url": edit_url, "project":project}


    
def do_commit(request, content):
    project = request.matchdict['project']
    page = request.matchdict['page']
    
    #construction of the wiki path
    wikiroot = request.registry.settings['wiki.root']  #from settings in .ini file.
    wikipath = os.path.join(wikiroot, project) #project name is the name of the git repository
    rootfilepath = os.path.join(wikipath, page) #we want one specific file into this directory
    
    files = glob.glob(rootfilepath+".*")  #list files with any extension
    log.debug(files)
    f = files[0]   #we take the first matching file, undertermined results if two files only differs by extension

    handle = open(f, "w")
    handle.write(content.encode('utf-8'))
    handle.close()
    
    log.debug('wrote this content: ' + content + " in file: " + f)
    
    repo = Repo(wikipath)
    strfilename = str(os.path.split(f)[1])
    
    repo.stage([strfilename])
    
    userinfos = get_user_infos(request)
    
    repo.do_commit("edited online with pygiwi", committer="%(name)s <%(email)s>"%userinfos)
    
    
    
@view_config(route_name = "edit", renderer = "pygiwi:templates/editpage.mako", permission="edit")
def edit_wiki(request):
    """this view displays the raw content of the edited file for editing
    """ 
    log.debug("calling edit_wiki")
    project = request.matchdict["project"]
    page = request.matchdict["page"]
    
    if "content" in request.POST:
        log.debug("content in request POST" + request.POST["content"])
        do_commit(request, request.POST['content'])
        return HTTPFound(custom_route_path(request, 'view_wiki', project=project, page=page)  )
        
            
        
    #create list of wikis:
    wikiroot = request.registry.settings['wiki.root']  #from settings in .ini file.
    wikis = os.listdir(wikiroot)
    
    content,ext = getPage(request, project, page)
    content = unicode(content, 'utf-8')
    
    return {"wikis": wikis, "project": project, "content": content}

    
@notfound_view_config(route_name="view_wiki", renderer="pygiwi:templates/wikipagenotfound.mako")
def wiki_not_found_view(exc, request):
    
    pagename = request.matchdict["page"]
    project = request.matchdict["project"]       
           
    mydict = dict(pagename = pagename, url=request.route_path('createpage', project=project, page=pagename))
    
    request.response.status = 404    
    
    return mydict
    
    
@view_config(route_name="createpage", permission="edit")
def create_wiki(request):
    
    project = request.matchdict['project']
    page = request.matchdict['page']
    wikiroot = request.registry.settings['wiki.root']
    
    #determine the new page path:
    rootpath = os.path.join(wikiroot, project)
    filepath = os.path.join(rootpath,page)
    filepath += ".md"  #TODO: markdown only for the moment
    
    #create the new page, and parent directories if needed
    
    if "/" in page:
        dirname = os.path.split(page)[0]
        dirpath = os.path.join(rootpath, dirname)
        log.debug("creating directory %s"%dirpath)
        mkdir_p(dirpath)
        
    f = open(filepath, "w")
    f.write("please set some content here")
    f.close()
    
    return HTTPFound(custom_route_path(request, "edit", project=project, page=page))