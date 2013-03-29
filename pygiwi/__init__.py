from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPFound


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    
    config.add_route('wiki_home', '/wiki')
    config.add_route('wiki_home2', '/wiki/') #same route but with trailing slash

        
    config.add_route("view_wiki", "/wiki/{project}/{page:.*}")
    config.add_route('wiki_project_home', '/wiki/{project}')
    
    config.add_route("edit", "/edit/{project}/{page:.*}")
    
    config.scan()
    return config.make_wsgi_app()
