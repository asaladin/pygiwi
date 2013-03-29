from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route("view_wiki", "/wiki/{project}/{page:.*}")
    config.add_route("edit", "/edit/{project}/{page:.*}")
    
    config.scan()
    return config.make_wsgi_app()
