import uuid

from django import forms
from captcha.fields import CaptchaField

from .models import Post, Comment

class PostForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Post
        fields = ['title', 'content','is_published', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'imageInput', 'accept': 'image/*'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        
        
    
    
class CommentForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }   
        