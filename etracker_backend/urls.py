
from django.contrib import admin
from django.urls import path,include
from users import views as userviews
from rest_framework.routers import DefaultRouter
from expenses import views as expenseviews

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'expenses', expenseviews.ExpenseView, basename='expenses')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',userviews.RegistrationView.as_view(),name='register'),
    path('login/',userviews.LoginView.as_view(),name='login'),
    path('csrf/',userviews.CsrfTokenView.as_view(),name='csrfset'),
    path('logout/',userviews.LogoutView.as_view(),name='logout'),
    path('auth/check/',userviews.CheckAuthView.as_view(),name='authcheck'),
    path('',include(router.urls)) # for getting, updatting, deleting, creating users' expenses
    
]
