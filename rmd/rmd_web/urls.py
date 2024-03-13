from django.urls import path
from . import views

urlpatterns = [
    # GET
    path('', views.home, name='home'),
    path('home2/', views.home2, name='home2'),

    path('person/', views.createNewPerson, name='createnewperson'),
    path('search/', views.searchPerson, name='searchperson'),
    path('explore/', views.explore, name='explore'),
    
    
    # ROUTES FOR DATE
    path('create_person/', views.create_person, name='create_person'),
    path('viewperson/', views.view_person, name='viewperson'),
    path('viewperson/<int:person_id>/', views.view_person, name='viewperson'),
    path('create_post/<int:person_id>/', views.create_post, name='create_post'),
    path('add_comment/', views.add_comment, name='add_comment'),
    
    
    
    # POST
    
   
    # AUTHENTICATION
    path('register/', views.register, name='signup'),
    path('my-login/', views.my_login, name='my-login'),
    path('user-logout', views.user_logout, name="user-logout" ),
]