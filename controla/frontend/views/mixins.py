from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import resolve
from django.utils.decorators import method_decorator

from users.models import User


class BaseFrontendViewMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):

        if not self.has_permissions(request, **kwargs):
            raise PermissionDenied

        return super(BaseFrontendViewMixin, self).dispatch(request, *args, **kwargs)


    def render_to_response(self, context, **response_kwargs):
        response_kwargs['current_app'] = resolve(self.request.path).namespace
        return super(BaseFrontendViewMixin, self).render_to_response(context, **response_kwargs)


class ResponsableViewMixin(BaseFrontendViewMixin):

    def has_permissions(self, request, **kwargs):
        if not self.request.user.rol == User.RESPONSABLE:
            return False

        return True


class SupervisorViewMixin(BaseFrontendViewMixin):

    def has_permissions(self, request, **kwargs):
        if not self.request.user.rol == User.SUPERVISOR:
            return False

        return True
