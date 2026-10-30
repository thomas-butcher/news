from django.http import Http404
from django.views.generic import TemplateView

from . import nyt

# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"


class NytBaseView(TemplateView):
    template_name = "nyt_list.html"

    def fetch(self):
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        try:
            ctx["stories"] = self.fetch()
        except nyt.NytError as exc:
            ctx["stories"] = []
            ctx["error"] = str(exc)
        return ctx


class NytTopStoriesView(NytBaseView):
    sections = ["home", "world", "us", "politics", "business", "technology", "science", "health", "arts", "sports"]

    def fetch(self):
        section = self.kwargs.get("section", "home")
        if section not in self.sections:
            raise Http404("Unknown section")
        return nyt.top_stories(section)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["heading"] = f"Top Stories: {self.kwargs.get('section', 'home').title()}"
        ctx["sections"] = self.sections
        ctx["is_top"] = True
        return ctx


class NytMostPopularView(NytBaseView):
    periods = [1, 7, 30]

    def fetch(self):
        period = self.kwargs.get("period", 1)
        if period not in self.periods:
            raise Http404("Unknown period")
        return nyt.most_popular(period)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["heading"] = f"Most Popular: last {self.kwargs.get('period', 1)} day(s)"
        ctx["periods"] = self.periods
        return ctx
