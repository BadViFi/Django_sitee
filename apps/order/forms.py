from django import forms

from .models import Cart, Order


       
class CartAddProductForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('user', 'product', 'quantity')
        widgets = {
            'user': forms.HiddenInput(), # Поле user приймає значення з запиту, тому його не потрібно відображати на формі
            'product': forms.HiddenInput(),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100, 'value': 1})
        }
        
    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        
        if product.quantity < quantity:
            raise forms.ValidationError('На складі недостатньо товару')
        
        return cleaned_data
    
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'comment')


class CartUpdateForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('quantity',)
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        product = self.instance.product
        quantity = cleaned_data.get('quantity')

        if product.quantity < quantity:
            raise forms.ValidationError('На складі недостатньо товару')
        elif quantity < 1:
            raise forms.ValidationError('Кількість товару не може бути менше 1')

        return cleaned_data