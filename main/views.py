from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import requests
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
import json
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseForbidden

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
    # Cek apakah ini request AJAX
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            
            if is_ajax:
                return JsonResponse({
                    'success': True, 
                    'message': 'Akun berhasil dibuat!', 
                    'redirect': reverse('main:login')
                })

            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
        else:
            # Jika form tidak valid, kirim error sebagai JSON untuk AJAX
            if is_ajax:
                # Ambil error pertama untuk ditampilkan di toast
                first_error = next(iter(form.errors.values()))[0]
                return JsonResponse({'success': False, 'error': first_error}, status=400)
    
    # Untuk request GET atau POST non-AJAX yang gagal, render halaman seperti biasa
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    # Cek apakah ini request AJAX
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if is_ajax:
                return JsonResponse({
                    'success': True, 
                    'message': 'Login berhasil!', 
                    'redirect': reverse('main:show_main')
                })

            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            # Jika form tidak valid, kirim error sebagai JSON untuk AJAX
            if is_ajax:
                return JsonResponse({'success': False, 'error': 'Username atau password salah.'}, status=400)

    else: # Request GET
        form = AuthenticationForm(request)
   
    # Untuk request GET atau POST non-AJAX yang gagal, render halaman seperti biasa
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def delete_product(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=id)
        # Tambahkan cek keamanan
        if product.user != request.user:
             return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
        product.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)



@require_POST
@csrf_exempt  
def add_product_entry_ajax(request):
    form = ProductForm(request.POST or None)
    
    if form.is_valid():
        product = form.save(commit=False)
        if request.user.is_authenticated:
            product.user = request.user
        product.save()
        return JsonResponse({"success": True, "message": "Produk berhasil ditambahkan!"})
    else:
        # Kirim error validasi pertama ke frontend
        first_error = next(iter(form.errors.values()))[0] if form.errors else "Data tidak valid"
        return JsonResponse({"success": False, "error": first_error}, status=400)


def get_product(request, id):
    try:
        product = Product.objects.get(pk=id)
        # PERBAIKAN KEAMANAN: Hanya pemilik yang bisa ambil data untuk edit
        if product.user and product.user != request.user:
             return JsonResponse({'error': 'Unauthorized'}, status=403)
             
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)


def edit_product(request, id):
    try:
        product = get_object_or_404(Product, pk=id)
    except Product.DoesNotExist:
        return JsonResponse({"success": False, "error": "Produk tidak ditemukan"}, status=404)

    if request.method == "POST":
        # PERBAIKAN KEAMANAN: Cek kepemilikan
        if product.user and product.user != request.user:
            return JsonResponse({"success": False, "error": "Anda tidak punya izin mengedit produk ini"}, status=403)
            
        form = ProductForm(request.POST or None, instance=product)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "Produk berhasil diperbarui"})
        else:
            # Kirim error validasi pertama ke frontend
            first_error = next(iter(form.errors.values()))[0] if form.errors else "Data tidak valid"
            return JsonResponse({"success": False, "error": first_error}, status=400)
            
    # Jika bukan POST
    return JsonResponse({"success": False, "error": "Metode request tidak valid"}, status=405)

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source with fake browser headers
        response = requests.get(
            image_url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            },
            timeout=10
        )
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)
    
@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            

            name = strip_tags(data.get("name", ""))          # Ganti dari title
            description = strip_tags(data.get("description", "")) 
            price = int(data.get("price", 0))                # Tambahkan price
            category = data.get("category", "")
            thumbnail = data.get("thumbnail", "")
            is_featured = data.get("is_featured", False)
            user = request.user

            # Pastikan user sudah login
            if not user.is_authenticated:
                return JsonResponse({"status": "error", "message": "User not logged in"}, status=401)

            # Buat objek Product, bukan News
            new_product = Product(
                user=user,
                name=name,
                price=price,
                description=description,
                category=category,
                thumbnail=thumbnail,
                is_featured=is_featured,
            )
            new_product.save()

            return JsonResponse({"status": "success"}, status=200)
        
        except Exception as e:
            # Tangani error jika ada, misal data tidak valid
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    else:
        # Method bukan POST
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)
    
@login_required(login_url='/auth/login/')
def get_my_products_flutter(request):
    product_list = Product.objects.filter(user=request.user)
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