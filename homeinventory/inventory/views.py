from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin
from homeinventory.core.views import GenericActionConfirmationMixin

from homeinventory.inventory.models import Location, Category, Item
from homeinventory.inventory.models import ItemAttachment
from homeinventory.inventory.models import ItemPhoto

from homeinventory.inventory.forms import UserRegistrationForm
from homeinventory.inventory.forms import ItemAttachmentForm
from homeinventory.inventory.forms import PhotoAttachmentForm
from homeinventory.inventory.forms import CategoryForm
from homeinventory.inventory.forms import LocationForm, ItemForm

from homeinventory.inventory.filters import ItemFilter


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'inventory/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'inventory/register.html',
                      {'user_form': user_form})


#
# Location section
#

class LocationList(LoginRequiredMixin, ListView):
    model = Location
    paginate_by = 5

    def get_queryset(self):
        queryset = super(LocationList, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)

        q = self.request.GET.get("q")

        if q:
            return queryset.filter(name__icontains=q)

        return queryset


class LocationDetail(LoginRequiredMixin, DetailView):
    model = Location


class LocationCreate(LoginRequiredMixin, GenericActionConfirmationMixin,
                     CreateView):
    model = Location
    success_msg = "Location created!"
    form_class = LocationForm
    success_url = reverse_lazy('location-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(LocationCreate, self).form_valid(form)


class LocationUpdate(LoginRequiredMixin, GenericActionConfirmationMixin,
                     UpdateView):
    model = Location
    success_msg = "Location updated!"
    form_class = LocationForm
    success_url = reverse_lazy('location-list')


class LocationDelete(LoginRequiredMixin, GenericActionConfirmationMixin,
                     DeleteView):
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
        queryset = super(CategoryList, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)

        q = self.request.GET.get("q")

        if q:
            return queryset.filter(name__icontains=q)

        return queryset


class CategoryDetail(LoginRequiredMixin, DetailView):
    model = Category


class CategoryCreate(LoginRequiredMixin, GenericActionConfirmationMixin,
                     CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category-list')
    success_msg = "Category created!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CategoryCreate, self).form_valid(form)


class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category-list')
    success_msg = "Category updated!"


class CategoryDelete(LoginRequiredMixin, GenericActionConfirmationMixin,
                     DeleteView):
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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ItemList, self).get_context_data(**kwargs)

        item_filter = ItemFilter(self.request.GET, queryset=self.object_list)
        context['filter'] = item_filter
        return context


class ItemDetail(LoginRequiredMixin, DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super(ItemDetail, self).get_context_data(**kwargs)
        attachments = ItemAttachment.objects.filter(item=self.get_object())
        context['attachments'] = attachments
        photos = ItemPhoto.objects.filter(item=self.get_object())
        context['photos'] = photos
        return context


class ItemCreate(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('item-list')
    success_msg = "Item created!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ItemCreate, self).form_valid(form)


class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('item-list')
    success_msg = "Item updated!"


class ItemDelete(LoginRequiredMixin, GenericActionConfirmationMixin,
                 DeleteView):
    model = Category
    success_url = reverse_lazy('item-list')
    success_msg = "Item deleted!"


class ItemAttachmentView(LoginRequiredMixin, FormView):
    form_class = ItemAttachmentForm
    template_name = 'inventory/item_attachment_upload.html'
    success_url = reverse_lazy('item-detail')

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(Item, pk=self.kwargs.get('pk'))
        form = self.form_class(initial={"item_id": item.id})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('upload')
        item = get_object_or_404(Item, pk=request.POST.get("item_id", ""))
        self.success_url = item.get_absolute_url()

        if form.is_valid():
            for f in files:
                attachment = ItemAttachment(item=item, upload=f,
                                            user=self.request.user)
                attachment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def item_attachment_delete(request, pk):
    attachment = get_object_or_404(ItemAttachment, pk=pk)
    item = attachment.item
    attachment.upload.delete()
    attachment.delete()
    return redirect('item-detail', pk=item.pk)


class ItemPhotoView(LoginRequiredMixin, FormView):
    form_class = PhotoAttachmentForm
    template_name = 'inventory/item_photo_upload.html'
    success_url = reverse_lazy('item-detail')

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(Item, pk=self.kwargs.get('pk'))
        form = self.form_class(initial={"item_id": item.id})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('upload')
        item = get_object_or_404(Item, pk=request.POST.get("item_id", ""))
        self.success_url = item.get_absolute_url()

        if form.is_valid():
            for f in files:
                photo = ItemPhoto(item=item, upload=f,
                                  user=self.request.user)
                photo.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def item_photo_delete(request, pk):
    photo = get_object_or_404(ItemPhoto, pk=pk)
    item = photo.item
    photo.upload.delete()
    photo.delete()
    return redirect('item-detail', pk=item.pk)
