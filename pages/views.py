from django.shortcuts import TemplateView

# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"