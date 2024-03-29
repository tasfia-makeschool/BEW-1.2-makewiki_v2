from django.test import TestCase
from django.contrib.auth.models import User
from wiki.models import Page
from wiki.forms import PageForm

# Create your tests here.
class WikiTestCase(TestCase):

    # canary test -- minimal tests that quickly verify that the system works as expected
    def test_true_is_true(self):
        """ Tests if True is equal to True. Should always pass. """
        self.assertEqual(True, True)
    
    # unit test, testing one behavior
    # in this case, testing if page is saved into database as expected
    def test_page_slugify_on_save(self):
        """ Tests the slug generated when saving a Page. """
        # Author is a required field in our model.
        # Create a user for this test and save it to the test database.
        user = User()
        user.save()

        # Create and save a new page to the test database.
        page = Page(title="My Test Page", content="test", author=user)
        page.save()

        # Make sure the slug that was generated in Page.save()
        # matches what we think it should be.
        self.assertEqual(page.slug, "my-test-page")

class PageListViewTests(TestCase):
    def test_multiple_pages(self):
        # Make some test data to be displayed on page
        user = User.objects.create()
        Page.objects.create(title="My Test Page", content="test", author=user)
        Page.objects.create(title="Another Test Page", content="test", author=user)
        
        # Issue a GET request to the MakeWiki homepage
        # When we make a request, we should get a response back
        response = self.client.get('/')

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the number of pages passed to the template matches
        # the number of pages we have in the database
        responses = response.context['pages']
        self.assertEqual(len(responses), 2)

        self.assertQuerysetEqual(
            responses,
            ['<Page: My Test Page>', '<Page: Another Test Page>'],
            ordered=False
        )

class PageDetailViewTests(TestCase):
    def test_detail_page(self):
        user = User.objects.create()
        page = Page.objects.create(title="My Test Page", content="test", author=user)
        page_slug = page.slug

        response = self.client.get(f'/{page_slug}/')

        self.assertEqual(response.status_code, 200)        

class PageCreateViewTests(TestCase):
    def test_form_loads(self):
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 200)   

    def test_create_new_page(self):
        pass

class PageFormTest(TestCase):
    def test_PageForm_valid(self):
        form = PageForm(data={'title': 'My New Page', 'content': 'test', 'author': 'spam'})
        self.assertTrue(form.is_valid())