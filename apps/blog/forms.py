import uuid

from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
   
    class Meta:
        model = Post
        fields = ['title', 'content','is_published', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        
    def save(self, commit=True):
        #rename image name
        post_instance = super(PostForm, self).save(commit=False)  # Get the instance of Post model
        
        # Rename image name if an image is uploaded
        if 'image' in self.cleaned_data:
            image = self.cleaned_data['image']
            new_image_name = f'{uuid.uuid4()}{image.name[image.name.rfind("."):]}'
            post_instance.image.name = new_image_name
        
        if commit:
            post_instance.save()
        return post_instance
        
        
    
    
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }   