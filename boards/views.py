from django.core import paginator
from django.http.response import Http404
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.urls import reverse


# Create your views here.

#from django.http import HttpResponse 
from .models import Board, Post, Topic

def home(request) :
    list_of_boards = Board.objects.all()
    
    return render(request, 'home.html', { 'boards' : list_of_boards})

class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset
@login_required
def new_topic(request, pk) : 
    board = get_object_or_404(Board, pk=pk)
    
    # Creating Functionality For Upcoming POST Requests
    if request.method == 'POST' :
        #subject = request.POST['subject']
        #message = request.POST['message']
        form = NewTopicForm(request.POST)
        
        if form.is_valid() : 
            topic = form.save(commit=False)
            
            
            topic.board = board
            topic.starter = request.user
            topic.save()
            
            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = request.user
            )
            
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)    
        
        
    else :
        
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board' : board, 'form': form})


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        # We don’t want to the same user refreshing the page counting as multiple views.
        # For this we can use sessions
        session_key = 'viewed_topic_{}'.format(self.topic.pk)  
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True 

        self.topic.views += 1
        self.topic.save()

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

@login_required
def reply_topic(request, pk, topic_pk) :
    print('Recieved Request')
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == "POST" :
        print('Recieved Request')
        form = PostForm(request.POST)
        if form.is_valid() :
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()  
            topic.save()
            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )
            print('topic', topic_post_url)
            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


#For Edit Option on user's created topic post
@method_decorator(login_required, name='dispatch') #class based views need a different way of decorator
class PostUpdateView(UpdateView) :
    model = Post
    fields = ['message',]
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def form_valid(self, form) :
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)