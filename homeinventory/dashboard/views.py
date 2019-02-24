import logging

from django.shortcuts import render
from django.http import JsonResponse

from django.db.models import Count

from homeinventory.inventory.models import Item, Category, Location, ItemLoan


logger = logging.getLogger(__name__)


def dashboard(request):
    # get loans
    item_loan = ItemLoan.objects \
                        .filter(item__user=request.user, returned=False) \
                        .order_by('-when')[:5]
    logger.debug(item_loan)
    # get next warranty expiring items
    item_warranty = Item.objects.filter(user=request.user, warranty=True) \
                                .order_by('warranty_expiration')[:5]
    logger.debug(item_warranty)
    return render(request,
                  'dashboard/dashboard.html',
                  {'item_loan': item_loan, 'item_warranty': item_warranty})


def total_item_by_category(request):
    q = Category.objects.filter(user=request.user) \
                        .annotate(data=Count('item')) \
                        .values('name', 'data').filter(data__gt=0)
    logger.debug(q)
    q_list = list(q)
    return JsonResponse(q_list, safe=False)


def total_item_by_location(request):
    q = Location.objects.filter(user=request.user) \
                        .annotate(data=Count('item')) \
                        .values('name', 'data').filter(data__gt=0)
    logger.debug(q)
    q_list = list(q)
    return JsonResponse(q_list, safe=False)
