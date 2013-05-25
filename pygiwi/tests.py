import unittest

from pyramid import testing
from dulwich.repo import Repo
import tempfile
import os
import shutil

from lib import mkdir_p

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        
        self.config.add_route('view_wiki', '/wiki/{project}/{page:.*}')
        self.config.add_route('edit', "/edit/{project}/{page:.*}")
        
        #create an empty repository
        self.tmpdir = tempfile.mkdtemp()
        self.repo = Repo.init(self.tmpdir)
        
        #populate with a new home page:
        with open("%s/%s"%(self.tmpdir, "Home.md"), "w") as f:
           f.write("hello wiki")   
        
        #create a page in a subdirectory as well
        mkdir_p("%s/%s"%(self.tmpdir, "testsubdir"))
        home_md = open("%s/%s"%(self.tmpdir, "testsubdir/subdirfile.md"), "w")
        home_md.write("hello subdir file")
        
        
        #add this new page to the revision history:
        self.repo.stage(["Home.md"])
        self.repo.do_commit("first revision", committer="john doe <john@doe.void>")
        
                
        request = testing.DummyRequest()
        self.root = os.path.split(self.tmpdir)[0]
        self.projectname = os.path.split(self.tmpdir)[1]
        
        request.registry.settings['wiki.root'] = self.root
        request.matchdict['page'] = "Home"
        request.matchdict['project'] = self.projectname
        
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
        
        #get the last commit:
        last_commit_id = self.repo.revision_history(self.repo.head())[0].id
        
        self.request.POST['content'] = "wiki2"
        
        #call the edit_wiki view to modify the home page
        p = edit_wiki(self.request)    
        
        #check for desired side effects
        #for example there should be a new commit        
        new_commit = self.repo.revision_history(self.repo.head())[0]
        self.assertNotEqual(last_commit_id, new_commit.id)
        self.assertEqual(last_commit_id, new_commit.parents[0])
        
        #check that the "Home.md" file was actually modified:
        home_md = open("%s/%s"%(self.tmpdir, "Home.md"), "r")
        self.assertIn("wiki2", home_md.read())
    
    def test_edit_wiki_subdirectory(self):
        """ test with a page in a subdir"""
        #TODO: writeme
        
        from .views import edit_wiki, view_wiki
        self.config.testing_securitypolicy(userid='john@doe.void',
                                           permissive=True)
        
        #get the last commit:
        last_commit_id = self.repo.revision_history(self.repo.head())[0].id
        
        self.request.POST['content'] = "subdir2"
        
        self.request.matchdict['page'] = "testsubdir/subdirfile.md"
        self.request.matchdict['project'] = self.projectname
                        

        #create the subdir file:
        from .views import create_wiki
        create_wiki(self.request)
                        
        #call the edit_wiki view to modify the home page
        p = edit_wiki(self.request)    
        
        #check for desired side effects
        #for example there should be a new commit        
        new_commit = self.repo.revision_history(self.repo.head())[0]
        self.assertNotEqual(last_commit_id, new_commit.id)
        self.assertEqual(last_commit_id, new_commit.parents[0])
        
        #check that the "Home.md" file was actually modified:
        home_md = open("%s/%s"%(self.tmpdir, "testsubdir/subdirfile.md"), "r")
        self.assertIn("subdir2", home_md.read())
        
        
    
    
    def test_edit_wiki_noUpdate(self):
        """test the edit wiki view but with a "get" request, ie no modification performed, just
        display the editor"""
        
        from .views import edit_wiki, view_wiki
        self.config.testing_securitypolicy(userid='john@doe.void',
                                           permissive=True)
        
        p = edit_wiki(self.request)
        self.assertIn(self.projectname, p['wikis'])
        self.assertEqual(self.projectname, p['project'])
        
    
    
    def test_wiki_home(self):
        """test the wiki_home view that basically lists all available wikis"""
        from .views import wiki_home
        
        #create a new empty request:
        request = testing.DummyRequest()
        request.registry.settings['wiki.root'] = self.root
        
        wh = wiki_home(self.request)
        self.assertIn(self.projectname, wh["wikis"])
