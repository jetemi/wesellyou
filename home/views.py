from django.views import generic

# Create your views here.
class HomePage(generic.TemplateView):
    '''Home Page view --> index.html'''
    template_name = 'home/index.html'