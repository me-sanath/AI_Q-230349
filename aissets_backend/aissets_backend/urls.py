from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/qna/', include('qna.urls')),
    path('api/auth/', include('auth.urls')),
]
