from os import name
from django.http import response
from django.urls import reverse, resolve
from django.test import TestCase

# Create your tests here.

from ..views import home
from ..models import Board


class HomeTest(TestCase) :
    # we prepare the environment to run the tests, so to simulate a scenario.
    def setUp(self) :
        self.board = Board.objects.create(name='Django', description="Django Board")
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self) :
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self) :
        view = resolve('/')
        self.assertEquals(view.func, home)
    
    # Here we are using the assertContains method to test if the response body contains a given text
    def test_home_view_contains_link_to_topic_page(self) :
        board_topics_url = reverse('board_topics', kwargs={'pk' : self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))



