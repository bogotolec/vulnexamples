import sys
from django.shortcuts import render
from django.views.debug import technical_500_response, technical_404_response
from hashlib import md5

from vulnexamples.views import MyFormView
from .forms import HashForm


class IndexView(MyFormView):
    template_name = 'a6_security_misconfiguration/index.html'
    form_class = HashForm

    def on_success(self, request):
        some_secret = 'some_secret'
        self.result = self.form.cleaned_data['text']
        for i in range(0, int(self.form.cleaned_data['times'])):
            self.result = md5(self.result.encode()).hexdigest()
        return self.render_form(request)

    def render_form(self, request):
        return render(request, self.template_name, {'form': self.form,
                                                    'result': getattr(self, 'result', '')})


def view404(request, exception):
    exc_type, exc_value, tb = sys.exc_info()
    return technical_404_response(request, exc_value)


def view500(request):
    return technical_500_response(request, *sys.exc_info())
