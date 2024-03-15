from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('',views.home,name='home'),

    path('vegetable/',views.VegetablesView.as_view(),name='vegetable'),
    path('groceryinfo/<int:id>/',views.GroceryinfoView.as_view(),name='groceryinfo'),
    path('addtocart/<int:id>/',views.add_to_cart,name='addtocart'),
    path('addcart/<int:id>/',views.addcart,name='addcart'),
    path('showcart/',views.show_cart,name='showcart'),
    path('addquantity/<int:id>/',views.add_quantity,name='addquantity'),
    path('minusquantity/<int:id>/',views.delete_quantity,name='minusquantity'),
    path('deletecart/<int:id>/',views.delete_cart,name='deletecart'),
    path('deleteaddress/<int:id>/',views.delete_address,name='deleteaddress'),




    path('registration/',views.registration,name='registration'),

    path('login/',views.log_in,name='login'),

    path('profile/',views.profile,name='profile'),

    path('address/',views.address,name='address'),

    path('logout/',views.log_out, name="logout"),

    path('changepassword/',views.changepassword, name="changepassword"),

    path('checkout/',views.checkout,name='checkout'),

    path('payment/',views.payment,name='payment'),
    
    path('payment_success/<int:selected_address_id>/',views.payment_success,name='paymentsuccess'),

    path('payment_failed/',views.payment_failed,name='paymentfailed'),

    path('order/',views.order,name='order'),

    path('buynow/<int:id>',views.buynow,name='buynow'),

    path('buynow_payment/<int:id>',views.buynow_payment,name='buynowpayment'),

    path('buynow_payment_success/<int:selected_address_id>/<int:id>',views.buynow_payment_success,name='buynowpaymentsuccess'),

   
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)