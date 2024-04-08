from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse

from django.shortcuts import render,redirect
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from apps.main.mixins import ListViewBreadcrumbMixin
from .forms import CartAddProductForm
from .models import Cart

# Create your views here.

class CartView(LoginRequiredMixin, ListViewBreadcrumbMixin):
    model = Cart
    template_name = 'order/cart.html'
    context_object_name = 'cart'
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).prefetch_related('product').prefetch_related('product__images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_price'] = sum([item.total_price() for item in self.get_queryset()])
        return context
    
    def get_breradcrumb(self):
        self.breadcrumbs = {
            'current': 'Кошик',
        }
        return self.breadcrumbs
    

class AddToCartView(LoginRequiredMixin, View):
    def get(self, request):
        data = request.GET.copy() # Копіюємо дані з запиту
        data.update(user=request.user)
        request.GET = data
        
        form = CartAddProductForm(request.GET)

        
        if form.is_valid():
            cart = form.save(commit=False)
            product_in_cart = Cart.objects.filter(user=request.user, product=cart.product).first()
            if product_in_cart:
                product_in_cart.quantity += cart.quantity
                product_in_cart.save()
                messages.success(request, f'Кількість товару {cart.product.name} збільшено на {cart.quantity} шт.')
                
            else:
                cart.save()
                messages.success(request, f'Товар {cart.product.name} додано в корзину')
            return redirect('catalog:product', slug=cart.product.slug, category_slug=cart.product.main_category().slug)
        else:
            messages.error(request, 'Помилка додавання товару в корзину')
            return redirect('catalog:index')
        
        
        
        
class DeleteFromCartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = kwargs.get('pk')
        cart = get_object_or_404(Cart, pk=cart_id)
        cart.delete()
        messages.success(request, f'Товар {cart.product.name} видалено з корзини')
        return redirect('order:cart')

class ClearCartView(LoginRequiredMixin, View):
    def get(self, request):
        Cart.objects.filter(user=request.user).delete()
        messages.success(request, 'Корзина очищена')
        return redirect('order:cart')


class CartOrderingView(CartView):
    template_name = 'order/cart_ordering.html'

    def get_breradcrumb(self):
        self.breadcrumbs = {
            f'{reverse("order:cart")}': 'Кошик',
            'current': 'Оформлення замовлення',
        }   
        return self.breadcrumbs