import logging
from django.shortcuts import render

from homeinventory.inventory.forms import UserRegistrationForm

logger = logging.getLogger(__name__)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            logger.info('New user created. Username: {0}, Email: {1}'
                        .format(new_user.username, new_user.email))
            return render(request, 'accounts/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'accounts/register.html',
                      {'user_form': user_form})
