from django.shortcuts import render, get_object_or_404
from .models import Product, Category



def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True) #фильтруем те что доступные по умолчанию

    category = None
    if category_slug: # если включается фильтрация:
        category = get_object_or_404(Category, slug=category_slug) # получает по условию что введеный фильтр(слаг) равен тому что уже есть в базе в таблице category со слагами(category_slug),проще говоря ищет фильтр введеный пользователем в тех что уже есть и прописанны в базе данных
        products = products.filter(category=category) # фильтруем по переменной что получили сверху,category=category просто фильтруем по этому условию,честно сам пока не до конца понимаю как это работает но допустим
    return render(request,  "main/product/list.html", # тут просто выводим,никакой магии
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True) # берем введенный продукт в переменную
    related_products = Product.objects.filter(category=product.category, # делаем "попробуйте также..." просто берем продукты из той же категории
                                               available=True).exclude(id=product.id)[:4] # что в данный момент доступны и исключаем уже введеный,и ограничиваем количество до 4
    return render(request, "main/product/base.html", {'product': product,
                                                        'related_product': related_products})