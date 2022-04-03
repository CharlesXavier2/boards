from django.http import response
from django.urls import reverse, resolve
from django.test import TestCase


from ..models import Board
from ..views import board_topics




class BoardTopicTests(TestCase) : 
    # we prepare the environment to run the tests, so to simulate a scenario.
    def setUp(self) :
        Board.objects.create(name='Django', description="Django Board")
    
    # testing if Django is returning a status code 200 (success) for an existing Board.
    def test_board_topics_view_successs_status_code(self) :
        url = reverse('board_topics', kwargs={'pk' : 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # testing if Django is returning a status code 404 (page not found) for a Board that doesn’t exist in the database.
    def test_board_topics_view_not_found_status_code(self) :
        url = reverse('board_topics', kwargs={'pk' : 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    # testing if Django is using the correct view function to render the topics.
    def test_board_topics_url_resolves_board_topics_view(self) :
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)

    def test_board_topics_view_contains_navigation_links(self) : 
        board_topics_url = reverse('board_topics', kwargs={"pk" : 1 })
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk' : 1})
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))
