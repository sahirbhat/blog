
from django.contrib import admin
from django.urls import path
from enroll import views
 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home ,name='home'),
    path('about/',views.about ,name='about'),
    path('contact/',views.contact ,name='contact'),
    path('dashboard/',views.dashboard ,name='dashboard'),
    path('logout/',views.logoutview ,name='logout'),
    path('signin/',views.signinview ,name='signin'),
    path('login/',views.loginview ,name='login'),
    path('addpost/',views.addpost,name='addpost'),
    path('update/<int:id>/',views.updatepost ,name='updatepost'),
    path('deletepost/<int:id>/',views.deletepost ,name='deletepost'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
          views.activate, name='activate'), 


    
]
