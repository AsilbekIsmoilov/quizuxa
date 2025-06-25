from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', lambda request: redirect('accounts:login')),

    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('app/', include('app.urls', namespace='app')),
]
