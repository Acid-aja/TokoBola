from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")
    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)
        
    context = {
        'npm' : '2406495786',
        'name': request.user.username,
        'class': 'PBP D',
        'product_list' : product_list,
        'last_login' : request.COOKIES.get('last_login', 'never')
    }

    return render(request, "main.html", context)

def add_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "add_product.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.increment_views()

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    data = [
        {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'category': product.category,
            'category_display': product.get_category_display(),
            'thumbnail': product.thumbnail,
            'views': product.views,
            'is_featured': product.is_featured,
            'user_id': product.user.id if product.user else None,
            'user_username': product.user.username if product.user else None,
        }
        for product in product_list
    ]

    return JsonResponse(data, safe=False)


def show_xml_by_id(request, Product_id):
   try:
       Product_list = Product.objects.filter(pk=Product_id)
       xml_data = serializers.serialize("xml", Product_list)
       return HttpResponse(xml_data, content_type="application/xml")
   except Product.DoesNotExist:
       return HttpResponse(status=404)

   
def show_json_by_id(request, Product_id):
    try:
        product = Product.objects.select_related('user').get(pk=Product_id)
        data = {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'category': product.category,
            'category_display': product.get_category_display(),  
            'thumbnail': product.thumbnail,
            'views': product.views,
            'is_featured': product.is_featured,
            'user_id': product.user.id if product.user else None,
            'user_username': product.user.username if product.user else None,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

# def edit_product(request, id):
#     product = get_object_or_404(Product, pk=id)
#     form = ProductForm(request.POST or None, instance=product)
#     if form.is_valid() and request.method == 'POST':
#         form.save()
#         return redirect('main:show_main')

#     context = {
#         'form': form
#     }

#     return render(request, "edit_product.html", context)

def delete_product(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=id)
        product.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@require_POST
@csrf_exempt
def add_product_entry_ajax(request):
    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else None
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        thumbnail = request.POST.get('thumbnail')
        category = request.POST.get('category')
        is_featured = request.POST.get('is_featured') == 'on'

        Product.objects.create(
            user=user,
            name=name,
            price=int(price),
            description=description,
            thumbnail=thumbnail,
            category=category,
            is_featured=is_featured,
        )
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "fail"}, status=400)

def get_product(request, id):
    from django.http import JsonResponse
    product = Product.objects.get(pk=id)
    return JsonResponse({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'description': product.description,
        'thumbnail': product.thumbnail,
        'category': product.category,
        'is_featured': product.is_featured,
    })

def edit_product(request, id):
    from django.http import JsonResponse
    if request.method == "POST":
        product = Product.objects.get(pk=id)
        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.description = request.POST.get("description")
        product.thumbnail = request.POST.get("thumbnail")
        product.category = request.POST.get("category")
        product.is_featured = bool(request.POST.get("is_featured"))
        product.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})