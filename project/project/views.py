from django.shortcuts import render
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic.edit import FormView

from allauth import app_settings as allauth_app_settings
from allauth.account import app_settings
from allauth.account.forms import (
    LoginForm,
)

from allauth.account.utils import (
    get_next_redirect_url,
    passthrough_next_redirect_url,
)
from allauth.core.exceptions import ImmediateHttpResponse
from allauth.utils import get_form_class, get_request_param
from allauth.account.views import (
    RedirectAuthenticatedUserMixin,
    AjaxCapableProcessFormViewMixin,
)

from cliente.models import Cliente


INTERNAL_RESET_SESSION_KEY = "_password_reset_key"

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters("oldpassword", "password", "password1", "password2")
)


def redirecionar(request):
    bd_cliente = Cliente.objects.filter(username=request.user)
    if request.user.is_authenticated:
        if request.user.is_staff:
            # Usuário é staff, redirecione para um template específico
            return render(request, "/account/index.html")
        elif bd_cliente:
            cliente = bd_cliente.values("id")[0]["id"]

            # Usuário comum, redirecione para o dashboard
            return render(request, f"/cliente/{cliente}/dashboard/")
    else:
        # Caso o usuário não esteja autenticado, redirecione para a página de login
        return render(request, "/")


class LoginView(
    RedirectAuthenticatedUserMixin, AjaxCapableProcessFormViewMixin, FormView
):
    form_class = LoginForm
    template_name = "account/login." + app_settings.TEMPLATE_EXTENSION
    success_url = None
    redirect_field_name = REDIRECT_FIELD_NAME

    @sensitive_post_parameters_m
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, "login", self.form_class)

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            return form.login(self.request, redirect_url=success_url)
        except ImmediateHttpResponse as e:
            return e.response

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = (
            get_next_redirect_url(self.request, self.redirect_field_name)
            or self.success_url
        )
        return ret

    def get_context_data(self, **kwargs):
        ret = super(LoginView, self).get_context_data(**kwargs)
        signup_url = passthrough_next_redirect_url(
            self.request, reverse("account_signup"), self.redirect_field_name
        )
        redirect_field_value = get_request_param(self.request, self.redirect_field_name)
        site = get_current_site(self.request)

        ret.update(
            {
                "signup_url": signup_url,
                "site": site,
                "redirect_field_name": self.redirect_field_name,
                "redirect_field_value": redirect_field_value,
                "SOCIALACCOUNT_ENABLED": allauth_app_settings.SOCIALACCOUNT_ENABLED,
            }
        )
        return ret


login = LoginView.as_view()
