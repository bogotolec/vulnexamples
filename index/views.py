from django.shortcuts import render
from django.views import generic


# Create your views here.
class IndexView(generic.View):

    template_name = 'index/index.html'

    def get(self, request):
        return render(request, self.template_name)