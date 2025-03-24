from django.urls import path
from book.view.adminview import *
from book.view.commonview import *

urlpatterns = [

    # URL's for Template Render and Redirect

    path('',home,name='home'),
    path('signin',signin,name='signin'),
    path('signup',signup,name='signup'),
    path('signout',signout, name='signout'),
    path('index',index,name='index'),
    path('bookform',bookform,name='bookform'),
    path('updatebook',updatebook,name='updatebook'),
    path('updatebook/<int:id>/', updatebook, name='updatebook'),
    path('deletebook/<int:id>/', deletebook, name='deletebook'),


    # URL's for API end points

    path('user-signup/', SignUpView.as_view(), name='user-signup'),
    path('user-signin/', SignInView.as_view(), name='user-signin'),
    path('manage-books/', BookManageView.as_view(), name='manage-books'),
    path('manage-books/<int:id>/', BookManageView.as_view(), name='manage-books'),

    
]