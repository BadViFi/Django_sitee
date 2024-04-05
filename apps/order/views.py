from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import CartAddProductForm
from .models import Cart

# Create your views here.
class AddToCartView(LoginRequiredMixin, View):
    def get(self, request):
        data = request.GET.copy() # Копіюємо дані з запиту
        data.update(user=request.user)
        request.GET = data

        form = CartAddProductForm(request.GET)


        if form.is_valid():
            cart = form.save()
            messages.success(request, f'Товар {cart.product.name} додано в корзину')
            return redirect('catalog:product', slug=cart.product.slug, category_slug=cart.product.main_category().slug)
        else:
            messages.error(request, 'Помилка додавання товару в корзину')
            return redirect('catalog:index')