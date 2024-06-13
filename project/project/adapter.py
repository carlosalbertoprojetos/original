from allauth.account.adapter import DefaultAccountAdapter


class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        from cliente.models import Cliente

        try:
            bd_cliente = Cliente.objects.get(email=request.user.username)
            if bd_cliente:
                path = f"/cliente/{bd_cliente.email}/dashboard/"
        except:
            path = "/index/"
        return path.format(username=request.user.username)
