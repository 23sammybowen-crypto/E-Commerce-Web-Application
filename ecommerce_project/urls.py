from django.contrib import admin
from django.urls import path, include
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('product/<int:id>/', views.product_detail, name='product-detail'),
    path('cart/', views.cart, name='cart'),
    path('add-product/', views.add_product, name='add-product'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add-to-cart'),
    path('decrease-from-cart/<int:product_id>/', views.decrease_from_cart, name='decrease-from-cart'),  
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),      

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)