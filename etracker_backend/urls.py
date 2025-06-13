
from django.contrib import admin
from django.urls import path
from users import views as userviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',userviews.RegistrationView.as_view(),name='register'),
    path('login/',userviews.LoginView.as_view(),name='login'),
    path('csrf/',userviews.CsrfTokenView.as_view(),name='csrfset'),
    path('logout/',userviews.LogoutView.as_view(),name='logout'),
    path('auth/check/',userviews.CheckAuthView.as_view(),name='authcheck')
    
]
