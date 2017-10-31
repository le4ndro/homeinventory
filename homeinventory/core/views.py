from django.shortcuts import render

class GenericActionConfirmationMixin:

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(GenericActionConfirmationMixin, self).form_valid(form)
