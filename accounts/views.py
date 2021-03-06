from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from .forms import SignUpForm
# Create your views here.
def signup(request) : 
    if request.method == "POST" :
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid() : 
            user = signup_form.save()
            login(request, user)
            return redirect('home')
    else:
        signup_form = SignUpForm()
    return render(request, 'signup.html', {'form': signup_form})


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user