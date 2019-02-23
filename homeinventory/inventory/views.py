import logging

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin
from homeinventory.core.views import GenericActionConfirmationMixin

from homeinventory.inventory.models import Location, Category, Item
from homeinventory.inventory.models import ItemAttachment, ItemLoan
from homeinventory.inventory.models import ItemPhoto


from homeinventory.inventory.forms import ItemAttachmentForm
from homeinventory.inventory.forms import PhotoAttachmentForm
from homeinventory.inventory.forms import CategoryForm
from homeinventory.inventory.forms import LocationForm, ItemForm, ItemLoanForm

from homeinventory.inventory.filters import ItemFilter

logger = logging.getLogger(__name__)


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
        loans = ItemLoan.objects.filter(item=self.get_object())
        context['loans'] = loans
        if loans:
            latest_loan = ItemLoan.objects.latest('id')
            context['can_loan'] = latest_loan.returned
        else:
            context['can_loan'] = True
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
    model = Item
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
    file_name = attachment.upload.name
    attachment.upload.delete()
    attachment.delete()
    logger.info("File {0} deleted by {1}.".format(file_name, request.user))
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
    file_name = photo.upload.name
    photo.upload.delete()
    photo.delete()
    logger.info("File {0} deleted by {1}.".format(file_name, request.user))
    return redirect('item-detail', pk=item.pk)


#
# ItemLoan section
#

class ItemLoanCreate(LoginRequiredMixin, FormView):
    form_class = ItemLoanForm
    template_name = 'inventory/item_loan_create.html'
    success_url = reverse_lazy('item-detail')

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(Item, pk=self.kwargs.get('pk'))
        form = self.form_class(initial={"item_id": item.id})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        item = get_object_or_404(Item, pk=request.POST.get("item_id", ""))
        self.success_url = item.get_absolute_url()

        if form.is_valid():
            new_item_loan = ItemLoan(item=item,
                                     who=form.cleaned_data['who'],
                                     when=form.cleaned_data['when'],
                                     why=form.cleaned_data['why'],
                                     expected_return_date=form.
                                     cleaned_data['expected_return_date']
                                     )
            new_item_loan.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def item_loan_returned(request, pk):
    loan = get_object_or_404(ItemLoan, pk=pk)
    item = loan.item
    loan.returned = True
    loan.save()
    logger.info("Item id: {0} returned in {1}. Updated by {2}"
                .format(item.id, loan.modified, request.user))
    return redirect('item-detail', pk=item.pk)
