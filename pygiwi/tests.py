import unittest

from pyramid import testing
from dulwich.repo import Repo
import tempfile
import os
import shutil


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        
        self.config.add_route('view_wiki', '"/wiki/{project}/{page:.*}')
        
        #create an empty repository
        self.tmpdir = tempfile.mkdtemp()
        repo = Repo.init(self.tmpdir)
        
        #populate with a new home page:
        with open("%s/%s"%(self.tmpdir, "Home.md"), "w") as f:
           f.write("hello wiki")   
                
        request = testing.DummyRequest()
        root = os.path.split(self.tmpdir)[0]
        projectname = os.path.split(self.tmpdir)[1]
        
        request.registry.settings['wiki.root'] = root
        request.matchdict['page'] = "Home"
        request.matchdict['project'] = projectname
        
        self.request = request
        

    def tearDown(self):
        testing.tearDown()
        try:
            shutil.rmtree(self.tmpdir)
        except:
            pass
        

    def test_my_view(self):
        from .views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['project'], 'pygiwi')

    def test_view_wiki(self):
        from .views import view_wiki
       
        page = view_wiki(self.request)
        self.assertIn("hello", page['content'])
        self.assertEqual(page["format"], "markdown")
    
        
    def test_edit_wiki(self):
        from .views import edit_wiki, view_wiki
        self.config.testing_securitypolicy(userid='john@doe.void',
                                           permissive=True)
        
        self.request.POST['content'] = "wiki2"
        p = edit_wiki(self.request)
        
        print p
        
