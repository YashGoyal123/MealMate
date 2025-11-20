"""
Forms for User Profile Management
"""
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile"""
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'bio', 'profile_picture'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'username': 'Username',
            'email': 'Email Address',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'bio': 'Bio',
            'profile_picture': 'Profile Picture',
        }
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        }

    def clean_email(self):
        """Ensure email is unique"""
        email = self.cleaned_data.get('email')
        user_id = self.instance.id
        
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise forms.ValidationError('This email is already in use.')
        
        return email
    
    def clean_username(self):
        """Ensure username is unique"""
        username = self.cleaned_data.get('username')
        user_id = self.instance.id
        
        if User.objects.filter(username=username).exclude(id=user_id).exists():
            raise forms.ValidationError('This username is already taken.')
        
        return username
