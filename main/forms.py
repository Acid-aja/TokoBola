from django.forms import ModelForm
from main.models import Product
from django import forms

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "thumbnail", "category", "is_featured"]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'bg-gray-800 text-white border border-red-600 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-600 w-full'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'bg-gray-800 text-white border border-red-600 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-600 w-full'
            }),
            'description': forms.Textarea(attrs={
                'class': 'bg-gray-800 text-white border border-red-600 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-600 w-full'
            }),
            'thumbnail': forms.Textarea(attrs={
                'class': 'bg-gray-800 text-white border border-red-600 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-600 w-full'
            }),
        }

