from django.contrib import messages
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse
from django.contrib.auth.views import logout as django_logout

from dj_utils.views import AuthenticatedMixin
from users.models import User


class RedirectRolView(AuthenticatedMixin, RedirectView):
    """
    """
    permanent = False

    def get_redirect_url(self, **kwargs):
        if self.request.user.rol == User.RESPONSABLE:
            return reverse(
                'responsable_frontend:index',

            )
        if self.request.user.rol == User.SUPERVISOR:
            return reverse(
                'admin:index',

            )


def logout(request):
    messages.add_message(request, messages.SUCCESS, u"Has cerrado la sesión exitosamente.")
    return django_logout(request, next_page=reverse('login'))


index = RedirectRolView.as_view()
