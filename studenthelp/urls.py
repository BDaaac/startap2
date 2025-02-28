from django.contrib import admin
from django.urls import path, include
from accounts import views  # ✅
from main.views import menu
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # маршруты для регистрации и логина
    path('', include('main.urls')),  # маршруты для главной страницы
    path('register/', views.register, name='register'),  # Добавь эт
    path('menu/', menu, name='menu'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)