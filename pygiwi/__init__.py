from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPFound

import pyramid.exceptions

from pyramid.events import subscriber
from pyramid.events import NewRequest

from pyramid.security import authenticated_userid

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory="pygiwi.security.RootFactory")
    
    #pyramid_persona adds ACLAuthorizationPolicy, AuthTktAuthenticationPolicy, and UnencryptedCookieSessionFactoryConfig
    config.include("pyramid_persona")
    
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    
    config.add_route('wiki_home', '/wiki')
    config.add_route('wiki_home2', '/wiki/') #same route but with trailing slash

        
    config.add_route("view_wiki", "/wiki/{project}/{page:.*}")
    config.add_route('wiki_project_home', '/wiki/{project}')
    
    config.add_route("edit", "/edit/{project}/{page:.*}")
    config.add_route("createpage", "/createpage/{project}/{page:.*}")
    config.add_route("preview", "/preview")
    
    
    config.add_view(".views.forbidden", context=pyramid.exceptions.Forbidden, renderer="pygiwi:templates/forbidden.mako")
    
    
    config.scan()
    return config.make_wsgi_app()

    
@subscriber(NewRequest)
def mysubscriber(event):
    event.request.user = authenticated_userid(event.request)