from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('indexz', views.index, name='index'),
    path('signinz', views.signin, name='signin'),
    path('signupz', views.signup, name='signup'),
    path('loutz', views.lout, name='lout'),
    path('chocolatez', views.chocolate, name='chocolate'),
    path('cakez', views.cake, name='cake'),
    path('chocolate_infoz/<int:id>', views.chocolate_info, name='chocolate_info'),
    path('cake_infoz/<int:id>', views.cake_info, name='cake_info'),
    path('cartz', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>', views.remove_from_cart, name='remove_from_cart'),
    path('checkoutz', views.checkout, name='checkout'),
    path('order-successz', views.order_success, name='order_success'),
    path('billz', views.show_bill, name='show_bill'),
    path('aboutz', views.about, name='about'),
    path('galleryz', views.gallery, name='gallery'),
    path('contactz', views.contact, name='contact'),
    path('success', views.contact_success, name='contact_success'),
    path('searchz', views.search, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
