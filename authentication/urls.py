from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('l', views.l, name='l'),
    path('lost', views.lost, name='lost'),
    path('found', views.found, name='found'),
    path('signout', views.signout, name='signout'),
    # Add the following two lines for lost.html and found.html
    path('lost.html', views.lost, name='lost-html'),
    path('found.html', views.found, name='found-html'),
    # URL for the contact page
    path('signin.html', views.signin, name='signin'),
     path('about.html', views.about, name='about'),
    path('contact.html', views.contact_page, name='contact'),
     path('l.html', views.l, name='l'),
    path('saveenqiry',views.saveenqury,name="saveenqiry"),
     path('save_lost_item',views.save_lost_item,name="save_lost_item"),
      path('save_found_item',views.save_found_item,name="save_found_item"),
    path('thank_you', views.thank_you, name='thank_you'),
     path('phone.html', views.phone_page, name='phone-html'), 
     path('response', views.response, name='response'),
]
