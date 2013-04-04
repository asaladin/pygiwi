from pyramid.security import authenticated_userid

from markdown import markdown
from creole import creole2html

import os, errno #for mkdir_p

#renderers:

def markdown_renderer(text):
    return markdown(text, extensions=['extra', 'codehilite'])
    
def creole_renderer(text):
    return creole2html(unicode(text))

#dict to select the correct renderer:
renderers = {
              ".md": markdown_renderer,
              ".wiki": creole_renderer,
             }

formats = {
           ".md": "markdown",
           ".wiki": "creole",
          }

          
def get_user_infos(request):
    userid = authenticated_userid(request)
        
    return {'name': 'Online User', 'email': userid}

    

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
    