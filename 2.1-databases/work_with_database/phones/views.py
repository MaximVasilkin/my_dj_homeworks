from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort_by = request.GET.get('sort', 'name')
    phones = list(Phone.objects.all())

    if sort_by == 'name':
        phones.sort(key=lambda x: x.name)
    elif sort_by == 'min_price':
        phones.sort(key=lambda x: x.price)
    elif sort_by == 'max_price':
        phones.sort(key=lambda x: x.price, reverse=True)

    template = 'catalog.html'
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    context = {'phone': Phone.objects.filter(slug=slug)[0]}
    return render(request, template, context)
