from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.models import User
from decimal import Decimal
import json

from .forms import CartAddProductForm, OrderCreateForm, CartUpdateForm
from .models import Cart, OrderProduct, Order

def discount(username):
    with open('users.json', 'r') as file:
        data = json.load(file)
        for user_data in data:
            if user_data['database_username'] == username:
                return True
    return False

def get_cart_data(user_id):
    user = User.objects.get(id=user_id)
    username = user.username
    cart = Cart.objects.filter(user=user_id).prefetch_related('product').prefetch_related('product__images')
    total_price = sum([item.total_price() for item in cart])

    # Проверяем, есть ли скидка для текущего пользователя
    discounted = discount(username)

    # Если скидка есть и у заказа не применялась, применяем ее к общей стоимости
    if discounted and not Order.objects.filter(user=user, discount_applied=False).exists():
        total_price = total_price * Decimal('0.95') 
        print("После скидки:", total_price)  # Применяем скидку 5%

    return {'cart': cart, 'total_price': total_price, 'discounted': discounted}

class CartView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'order/cart.html'
    context_object_name = 'cart'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).prefetch_related('product').prefetch_related('product__images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_data = get_cart_data(self.request.user.id)
        context['cart'] = cart_data['cart']
        context['total_price'] = cart_data['total_price']
        context['discounted'] = cart_data['discounted']
        context['total_price_without_discount'] = sum([item.total_price() for item in cart_data['cart']])
        return context

class AddToCartView(LoginRequiredMixin, View):
    def get(self, request):
        data = request.GET.copy() 
        data.update(user=request.user)
        request.GET = data
        form = CartAddProductForm(request.GET)

        if form.is_valid():
            cart = form.save(commit=False)
            product_in_cart = Cart.objects.filter(user=request.user, product=cart.product).first()
            if product_in_cart:
                product_in_cart.quantity = cart.quantity
                product_in_cart.save()
                messages.success(request, f'Кількість товару {cart.product.name} змінено на {cart.quantity}')
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_data = get_cart_data(self.request.user.id)
        context['cart'] = cart_data['cart']
        context['total_price'] = cart_data['total_price']
        context['form'] = OrderCreateForm()
        return context

    def post(self, request):
        cart_data = get_cart_data(request.user.id)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user


            if not order.discount_applied:
                discounted = discount(request.user.username)
                if discounted:
                    total_price = cart_data.get('total_price') * Decimal('0.95') 
                    total_price += total_price * Decimal('0.05')
                else:
                    total_price = cart_data.get('total_price')
                order.total_price = total_price
                order.discount_applied = True 
                order.save()

            with transaction.atomic():
                for item in cart_data.get('cart'):
                    order_product = OrderProduct(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price)
                    order_product.save()
                    item.product.quantity -= item.quantity
                    item.product.save()
                Cart.objects.filter(user=request.user).delete()

            messages.success(request, 'Замовлення успішно оформлено')
            return redirect('order:complete', order_id=order.id)
        else:
            messages.error(request, f'Помилка оформлення замовлення: {form.errors}')
            return redirect('order:cart_ordering')



class OrderComplete(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order = Order.objects.get(pk=order_id)

        context = {
            'order': order,
            'total_price': order.total_price,
        }
        return render(request, 'order/order_complete.html', context=context)

    def post(self, request):
        return redirect('order:cart')


class CartUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = kwargs.get('cart_id')
        action = kwargs.get('action')
        cart = get_object_or_404(Cart, pk=cart_id)
        if action == 'add':
            cart.quantity += 1
            cart.save()
        elif action == 'remove':
            cart.quantity -= 1
            if cart.quantity == 0:
                cart.quantity = 1
                messages.error(request, f'Кількість товару {cart.product.name} не може бути менше 1')
            cart.save()

        if cart.quantity > cart.product.quantity:
            messages.add_message(request, messages.ERROR, f'На складі недостатньо товару {cart.product.name}', extra_tags='danger')
            cart.quantity = cart.product.quantity
            cart.save()
            return redirect('order:cart')
        messages.success(request, f'Кількість товару {cart.product.name} змінено на {cart.quantity}')

        return redirect('order:cart')

    def post(self, request, *args, **kwargs):
        cart_id = kwargs.get('cart_id')
        cart = get_object_or_404(Cart, pk=cart_id)

        form = CartUpdateForm(request.POST, instance=cart)

        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')
            cart.quantity = quantity
            cart.save()
            messages.success(request, f'Кількість товару {cart.product.name} змінено на {quantity}')
        else:
            messages.error(request, f'Помилка зміни кількості товару: {[error for error in form.errors.values()][0][0]}', extra_tags='danger')

        return redirect('order:cart')
