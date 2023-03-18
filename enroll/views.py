from django.shortcuts import render,HttpResponsePermanentRedirect,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from . forms import UserSignInForm,PostForm
from django.contrib import messages
from . models import Post


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
   fm.save()
   messages.success(request,'Your Ac has been Created Successfully')
   
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
        
            
    