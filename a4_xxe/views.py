from lxml import etree
from lxml.etree import ParseError, XMLParser
from django.shortcuts import render

from vulnexamples.views import MyFormView
from vulnexamples.forms import FileUploadForm
from .resolvers import OnlyOneURLResolver


class IndexView(MyFormView):
    DEFAULT_SIZE = 20
    DEFAULT_MINES = 50

    template_name = 'a4_xxe/index.html'
    form_class = FileUploadForm

    def validate(self, request):
        self.form.errors['file'] = self.form.errors.get('file', [])
        try:
            parser = XMLParser(resolve_entities=True)
            parser.resolvers.add(OnlyOneURLResolver())
            xml = etree.parse(request.FILES.get('file'), parser=parser).getroot()
            self.mines = getattr(xml.find('mines'), "text", self.DEFAULT_MINES)
            self.size = getattr(xml.find('size'), "text", self.DEFAULT_SIZE)
        except ParseError as e:
            self.form.errors['file'] += [str(e)]

    def on_success(self, request):
        return self.render_form(request)

    def render_form(self, request):
        return render(request, self.template_name,
                      {'form': self.form,
                       'mines': getattr(self, 'mines', self.DEFAULT_MINES),
                       'size': getattr(self, 'size', self.DEFAULT_SIZE)})


def settings(request):
    return render(request, 'a4_xxe/settings.xml', content_type='text/xml')
