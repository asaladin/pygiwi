import unittest

from pyramid import testing
from dulwich.repo import Repo
import tempfile
import os
import shutil


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

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
        
        #create an empty repository
        self.tmpdir = tempfile.mkdtemp()
        repo = Repo.init(self.tmpdir)
        
        #populate with a new home page:
        with open("/tmp/testwiki/Home.md", "w") as f:
           f.write("hello wiki")
                
        request = testing.DummyRequest()
        root = os.path.split(self.tmpdir)[0]
        request.registry.settings['wiki.root'] = root
        request.matchdict['page'] = "Home"
        request.matchdict['project'] = "testwiki"
                
        page = view_wiki(request)
        self.assertIn("hello", page['content'])
        self.assertEqual(page["format"], "markdown")