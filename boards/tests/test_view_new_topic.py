from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth.models import User



from ..forms import NewTopicForm
from ..models import Board, Post, Topic
from ..views import new_topic



class NewTopicTests(TestCase) : 
    # we prepare the environment to run the tests, so to simulate a scenario.
    def setUp(self) :
        Board.objects.create(name='Django', description="Django Board")
        User.objects.create_user(username='Abhinav', email='abhinav@django.com', password='12345')
    # testing if Django is returning a status code 200 (success) for an existing Board.
    def test_new_topic_view_successs_status_code(self) :
        url = reverse('new_topic', kwargs={'pk' : 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # testing if Django is returning a status code 404 (page not found) for a Board that doesn’t exist in the database.
    def test_new_topic_view_not_found_status_code(self) :
        url = reverse('new_topic', kwargs={'pk' : 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    # testing if Django is using the correct view function to render the topics.
    def test_new_topic_url_resolves_new_topic_view(self) :
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics(self) : 
        new_topic_url = reverse('new_topic', kwargs={"pk" : 1 })
        response = self.client.get(new_topic_url)
        board_topics_url = reverse('board_topics', kwargs={"pk" : 1 })
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))


    ### Following are the tests written for the New Topics Form

    def test_csrf(self) : 
        url = reverse('new_topic', kwargs={'pk' : 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_contains_form(self):  # <- new test
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    
    #sends a valid combination of data and check if the view created a Topic instance and a Post instance.
    def test_new_topic_valid_post_data(self) :
        url = reverse('new_topic', kwargs={'pk' : 1})
        data = {
            'subject' : 'Test Subject',
            'message' : 'Test Message'
        }

        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    #here we are sending an empty dictionary to check how the application is behaving.
    def test_new_topic_invalid_post_data(self) : 
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk' : 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertTrue(form.errors)
        self.assertEquals(response.status_code, 200)


        

    #The application is expected to validate and reject empty subject and message.
    def test_new_topic_invalid_post_data_empty_fields(self) : 
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject' : '',
            'message' : ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())



class LoginRequiredNewTopicTests(TestCase) :
    def setUp(self) : 
        Board.objects.create(name='Django', description='Django board.')
        self.url = reverse('new_topic', kwargs={'pk': 1})
        self.response = self.client.get(self.url)
    

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
