from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Location, Category

from .forms import UserRegistrationForm

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

class LocationList(LoginRequiredMixin, ListView):
    model = Location
    def get_queryset(self):
        return Location.objects.filter(user=self.request.user)

class LocationDetail(LoginRequiredMixin, DetailView):
    model = Location

class LocationCreate(LoginRequiredMixin, CreateView):
    model = Location
    fields = ['name', 'description']
    success_url = reverse_lazy('location-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(LocationCreate, self).form_valid(form)

class LocationUpdate(LoginRequiredMixin, UpdateView):
    model = Location
    fields = ['name', 'description']
    success_url = reverse_lazy('location-list')

class LocationDelete(LoginRequiredMixin, DeleteView):
    model = Location
    success_url = reverse_lazy('location-list')


class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class CategoryDetail(LoginRequiredMixin, DetailView):
    model = Category

class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'description']
    success_url = reverse_lazy('category-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CategoryCreate, self).form_valid(form)

class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'description']
    success_url = reverse_lazy('category-list')

class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('category-list')
