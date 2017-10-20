from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Location, Category, Item

from .forms import UserRegistrationForm

#
# Shared section
#

class GenericActionConfirmationMixin:

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(GenericActionConfirmationMixin, self).form_valid(form)

#
# General section
#

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'inventory/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'inventory/register.html', {'user_form': user_form})


#
# Location section
#

class LocationList(LoginRequiredMixin, ListView):
    model = Location
    paginate_by = 5

    def get_queryset(self):
        return Location.objects.filter(user=self.request.user)

class LocationDetail(LoginRequiredMixin, DetailView):
    model = Location

class LocationCreate(LoginRequiredMixin, GenericActionConfirmationMixin, CreateView):
    model = Location
    success_msg = "Location created!"

    fields = ['name', 'description']
    success_url = reverse_lazy('location-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(LocationCreate, self).form_valid(form)

class LocationUpdate(LoginRequiredMixin, GenericActionConfirmationMixin, UpdateView):
    model = Location
    success_msg = "Location updated!"

    fields = ['name', 'description']
    success_url = reverse_lazy('location-list')

class LocationDelete(LoginRequiredMixin, GenericActionConfirmationMixin, DeleteView):
    model = Location
    success_url = reverse_lazy('location-list')
    success_msg = "Location deleted!"

#
# Category section
#

class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    paginate_by = 5

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class CategoryDetail(LoginRequiredMixin, DetailView):
    model = Category

class CategoryCreate(LoginRequiredMixin, GenericActionConfirmationMixin, CreateView):
    model = Category
    fields = ['name', 'description']
    success_url = reverse_lazy('category-list')
    success_msg = "Category created!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CategoryCreate, self).form_valid(form)

class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'description']
    success_url = reverse_lazy('category-list')
    success_msg = "Category updated!"

class CategoryDelete(LoginRequiredMixin, GenericActionConfirmationMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('category-list')
    success_msg = "Category deleted!"

#
# Item section
#

class ItemList(LoginRequiredMixin, ListView):
    model = Item
    paginate_by = 5

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

class ItemDetail(LoginRequiredMixin, DetailView):
    model = Item

class ItemCreate(LoginRequiredMixin, CreateView):
    model = Item
    fields = [
                'make',
                'model',
                'id_number',
                'purchased_from',
                'purchased_date',
                'quantity',
                'value',
                'estimated_current_value',
                'description',
                'attributes',
                'notes',
                'year',
                'category',
                'location',
                'warranty',
                'warranty_type',
                'warranty_expiration',
                'warranty_contact_info'
             ]
    success_url = reverse_lazy('item-list')
    success_msg = "Item created!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ItemCreate, self).form_valid(form)

class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = Item
    fields = [
                'make',
                'model',
                'id_number',
                'purchased_from',
                'purchased_date',
                'quantity',
                'value',
                'estimated_current_value',
                'description',
                'attributes',
                'notes',
                'year',
                'category',
                'location',
                'warranty',
                'warranty_type',
                'warranty_expiration',
                'warranty_contact_info'
             ]
    success_url = reverse_lazy('item-list')
    success_msg = "Item updated!"

class ItemDelete(LoginRequiredMixin, GenericActionConfirmationMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('item-list')
    success_msg = "Item deleted!"
