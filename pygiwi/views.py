from pyramid.view import view_config

from markdown import *



@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'pygiwi'}

@view_config(route_name="view_wiki", renderer="pygiwi:templates/wiki.mako")
def view_wiki(request):
	pagename = request.matchdict["page"]
	project = request.matchdict["project"]
	
	text = open("/home/saladin/Src/Web/Pyramid/testwiki/%s.md"%pagename, 'r').read()
	
	html = markdown(text, extensions=['extra', 'codehilite'])
	
	return {"wikis": ["un", "deux"], "content": html}