
from markdown import markdown
from creole import creole2html


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

