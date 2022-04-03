from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse 

def products_home(*args, **kwargs) :
    
    response_html = '''<p>Abhinav's Work</p><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1M1MLou_lxL_Aj1m4tS1jDOvEDJxGrEph7g&usqp=CAU" height="200" width="350" />'''
    return HttpResponse(response_html)