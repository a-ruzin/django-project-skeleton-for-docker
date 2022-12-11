from django.views.generic import TemplateView

from django.conf import settings


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["domain"] = settings.PROJECT_DOMAIN
        return context
