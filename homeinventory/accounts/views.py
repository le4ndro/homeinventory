import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.urls import reverse_lazy

from homeinventory.accounts.forms import UserRegistrationForm
from homeinventory.accounts.forms import EditEmailForm

logger = logging.getLogger(__name__)


def register(request):
    logger.info('Entering register view')
    if request.method == 'POST':
        logger.info('is a post!')
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            logger.info('the form is valid!')
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            logger.info('New user created. Username: {0}, Email: {1}'.format(new_user.username, new_user.email))
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'user_form': user_form})


@login_required
def my_account(request):
    return render(request, 'accounts/my_account.html')


class EditEmailView(LoginRequiredMixin, FormView):
    form_class = EditEmailForm
    template_name = 'accounts/edit_email.html'
    success_url = reverse_lazy('my-account')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            email = form.cleaned_data["new_email1"]
            self.request.user.email = email
            self.request.user.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
