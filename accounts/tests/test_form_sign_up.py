from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.http import response
from django.test import TestCase


from ..views import signup
from ..forms import SignUpForm

# Create your tests here.

class SignUpFormTest(TestCase) : 
    def test_form_has_fields(self) : 
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)