from django import forms
from django.forms import fields
from django.forms.widgets import Textarea
from .models import Post, Topic

class NewTopicForm(forms.ModelForm) : 
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': "What's in your mind?" }
        ),
        max_length=4000,
        help_text='The max length can be 4000' 
        )
        

    class Meta : 
        model = Topic
        fields = ['subject', 'message']

class PostForm(forms.ModelForm) :
    class Meta :
        model = Post
        fields = ['message']       