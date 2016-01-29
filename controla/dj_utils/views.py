from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class AuthenticatedMixin(object):
    """
    View mixin which verifies that the user has authenticated.
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AuthenticatedMixin, self).dispatch(*args, **kwargs)
