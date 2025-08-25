from django.shortcuts import render, redirect, get_object_or_404
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    phones = Phone.objects.all()
    sort_param = request.GET.get('sort')
    if sort_param == 'name':
        phones = phones.order_by('name')
    elif sort_param == 'min_price':
        phones = phones.order_by('price')
    elif sort_param == 'max_price':
        phones = phones.order_by('-price')
    else:
        # по умолчанию оставляем порядок сортировки неизмененным
        pass
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    phone = get_object_or_404(Phone, slug=slug)
    template = 'product.html'
    context = {'phone': phone}
    return render(request, template, context)
