from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView


from .forms import UserRegisterCreationForm

class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterCreationForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = form.save()

        send_mail(
            subject='Добро пожаловать!',
            message='Спасибо за регистрацию на нашем сайте.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list = [user.email],

        )
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('catalog:home')


class CustomLogoutView(LogoutView):
    template_name = 'logout.html'