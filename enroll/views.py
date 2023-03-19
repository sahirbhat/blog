from django.shortcuts import render,HttpResponsePermanentRedirect,HttpResponseRedirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from . forms import UserSignInForm,PostForm
from django.contrib import messages
from . models import Post
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode ,urlsafe_base64_decode  
from django.template.loader import render_to_string  
# from .token import account_activation_token  
from django.core.mail import EmailMessage  
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator


# Create your views here.
def home(request):
    post=Post.objects.all()
    return render (request,'blog/home.html',{'post':post})




def about(request):
 return render (request,'blog/about.html')

def contact(request):
 return render (request,'blog/contact.html')


def dashboard(request):
 if request.user.is_authenticated:
    post=Post.objects.all()
    return render (request,'blog/dashboard.html',{'post':post})
 else:
   return HttpResponseRedirect('/login/')

def signinview(request):
 if request.method=='POST':
  fm=UserSignInForm(request.POST)
  if fm.is_valid():
    # user=fm.save()
    user = fm.save(commit=False)  
    user.is_active = False  
    user.save() 
    group=Group.objects.get(name='Author')
    user.groups.add(group) 
        # to get the domain of the current site  
    current_site = get_current_site(request)  
    mail_subject = 'Activation link has been sent to your email id'  
    message = render_to_string('blog/acc_active_email.html',{  
    'user': user,  
    'domain': current_site.domain,  
    'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
    'token':default_token_generator.make_token(user) 
    })  
    to_email = fm.cleaned_data.get('email')  
    email = EmailMessage( 
            mail_subject, message, to=[to_email]  
    )
    email.send()  
  
    messages.success(request,'Your Ac has been Created Successfully!!!!! Verify Ur ac first ')
    HttpResponseRedirect('login/')
 else:  
     
  fm=UserSignInForm()
 return render (request,'blog/signin.html',{'fm':fm})

#LOginVIEW
def loginview(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                un=fm.cleaned_data['username']
                ps=fm.cleaned_data['password']  
                print(un,ps)
                user=authenticate(username=un,password=ps)
                if user is not None:
                    login(request,user)
                    messages.success(request,'login successfully')
                    return HttpResponseRedirect('/dashboard/')
        else:   
            fm=AuthenticationForm()
        return render (request,'blog/login.html',{'fm':fm})
    else:
        HttpResponseRedirect('/dashboard/')

 
 


def logoutview(request):
 logout(request)
 return HttpResponseRedirect('/')

def addpost(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm=PostForm(request.POST)
            if fm.is_valid():
                fm.save()
            HttpResponseRedirect('dashboard')
            messages.success(request,'Your Post Created Successfully')
        fm=PostForm()
        return render (request,'blog/signin.html',{'fm':fm})
    else:
       HttpResponseRedirect('/login/')


 




  
    
 


def updatepost(request,id):
  if request.user.is_authenticated:
    if request.user =="POST":
      pi=Post.object.get(pk=id)
      form=PostForm(request.POST ,instance=pi)
      if form.is_valid():
        form.save()
  else:
    pi=Post.object.get(pk=id) 
    form=PostForm(instance=pi)
    return render(request,'blog/addpost.html',{'form':form})



# def deletepost(request,id):
#     if request.method=='POST':
#         pi=Post.objects.get(pk=id)
#         print(pi,"_____________________________")
#         pi.delete()
#         return HttpResponseRedirect('/dashboard/')
#     else:
#       HttpResponseRedirect('/dashboard/')

def deletepost(request, id):
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return HttpResponseRedirect("Post not found")

    # Delete post with the given post_id
    post.delete()

    # Redirect to a success page
    return HttpResponseRedirect('/dashboard/')




def activate(request, uidb64, token):  
    # User = get_user_model()  
    try:  
        uid = str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')  
        
            
    