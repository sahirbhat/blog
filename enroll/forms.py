from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput,PasswordInput,Textarea
from django import forms
from . models import Post

class UserSignInForm(UserCreationForm): 
 password1=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class': 'form-control'}))
 password2=forms.CharField(label="Confirm password",widget=forms.PasswordInput(attrs={'class': 'form-control'}))
 class Meta:
        model=User
        fields=['username','first_name','last_name','email',]
        labels={'first_name':'First Name','last_name':'Last Name'}
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            
        }

class PostForm(forms.ModelForm) :
    
    class Meta:
        model=Post
        fields=['title','decscription']   
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'decscription': Textarea(attrs={'class': 'form-control'}),
           
            
        }


        
        
       

        