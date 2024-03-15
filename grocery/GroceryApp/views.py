from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from . models import Customer,Grocery,Order,Cart
from . forms import RegistrationForm,AuthenticateForm,ChangePasswordForm,UserProfileForm,AdminProfileForm,CustomerForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.db.models import F

#===============For Paypal =========================
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse


def home(request):
    return render(request,'app/home.html')



class VegetablesView(View):
    def get(self,request):
        vegetable = Grocery.objects.filter(category='VEGETABLES') 
        return render(request,'cart/vegetable_cart.html',{'vegetable':vegetable})







def registration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            mf = RegistrationForm(request.POST)
            if mf.is_valid():
                mf.save()
                return redirect('registration')    
        else:
            mf  = RegistrationForm()
        return render(request,'app/registration.html',{'mf':mf})
    else:
        return redirect('profile')

def log_in(request):
    if not request.user.is_authenticated:  
        if request.method == 'POST':       
            mf = AuthenticateForm(request,request.POST)
            if mf.is_valid():
                name = mf.cleaned_data['username']
                pas = mf.cleaned_data['password']
                user = authenticate(username=name, password=pas)
                if user is not None:
                    login(request, user)
                    return redirect('/')
        else:
            mf = AuthenticateForm()
        return render(request,'app/login.html',{'mf':mf})
    else:
        return redirect('profile')

def profile(request):
    if request.user.is_authenticated: 
        if request.method == 'POST':
            if request.user.is_superuser == True:
                mf = AdminProfileForm(request.POST,instance=request.user)
            else:
                mf = UserProfileForm(request.POST,instance=request.user)
            if mf.is_valid():
                mf.save()
        else:
            if request.user.is_superuser == True:
                mf = AdminProfileForm(instance=request.user)
            else:
                mf = UserProfileForm(instance=request.user)
        return render(request,'app/profile.html',{'name':request.user,'mf':mf})
    else:                                                
        return redirect('login')

def log_out(request):
    logout(request)
    return redirect('home')


def changepassword(request):                                                    
    if request.user.is_authenticated:                               
        if request.method == 'POST':                               
            mf =ChangePasswordForm(request.user,request.POST)
            if mf.is_valid():
                mf.save()
                update_session_auth_hash(request,mf.user)
                return redirect('profile')
        else:
            mf = ChangePasswordForm(request.user)
        return render(request,'app/changepassword.html',{'mf':mf})
    else:
        return redirect('login')
    
#=========================================================================================================================================
    
class GroceryinfoView(View):
    def get(self,request,id):     
        grocery = Grocery.objects.get(pk=id)

        if grocery.discounted_price !=0:  
            percentage = int(((grocery.selling_price - grocery.discounted_price) / grocery.selling_price)*100)
        else:
            percentage = 0
        return render(request,'app/groceryinfo.html',{'grocery': grocery , 'percentage':percentage})

def add_to_cart(request, id):    
    if request.user.is_authenticated:
        product = Grocery.objects.get(pk=id) 
        user=request.user                
        Cart(user=user,product=product).save()  
        return redirect('groceryinfo', id)       
    else:
        return redirect('login')

def addcart(request, id):    
    if request.user.is_authenticated:
        product = Grocery.objects.get(pk=id) 
        user=request.user                
        Cart(user=user,product=product).save()  
        return redirect('showcart')       
    else:
        return redirect('login')    
    
def show_cart(request):
    cart_items = Cart.objects.filter(user=request.user)      
    total =0
    delhivery_charge =50
    for item in cart_items: 
        item.product.price_and_quantity_total =  item.product.discounted_price * item.quantity 
        total += item.product.price_and_quantity_total
        GST = item.product.price_and_quantity_total * 0.06
    final_price= delhivery_charge + total + GST
    return render(request, 'app/showcart.html', {'cart_items': cart_items,'total':total,'final_price':final_price})

def add_quantity(request, id):
    product = get_object_or_404(Cart, pk=id)   
    product.quantity += 1                        
    product.save()
    return redirect('showcart')

def delete_quantity(request, id):
    product = get_object_or_404(Cart, pk=id)
    if product.quantity > 1:
        product.quantity -= 1
        product.save() 
    return redirect('showcart')

def delete_cart(request,id):
    if request.method == 'POST':
        de = Cart.objects.get(pk=id)
        de.delete()
    return redirect('showcart')

#======================================================================================================================================

def address(request):
    if request.method == 'POST':
            print(request.user)
            mf =CustomerForm(request.POST)
            if mf.is_valid():
                user=request.user               
                name= mf.cleaned_data['name']
                address= mf.cleaned_data['address']
                city= mf.cleaned_data['city']
                state= mf.cleaned_data['state']
                pincode= mf.cleaned_data['pincode']
                Customer(user=user,name=name,address=address,city=city,state=state,pincode=pincode).save()
                return redirect('address')           
    else:
        mf =CustomerForm()
        address = Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',{'mf':mf,'address':address})

def delete_address(request,id):
    if request.method == 'POST':
        de = Customer.objects.get(pk=id)
        de.delete()
    return redirect('address')

#=====================================================================================================

def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)     
    total =0
    delhivery_charge =50
    for item in cart_items:
        item.product.price_and_quantity_total = (item.product.discounted_price * item.quantity) 
        total += item.product.price_and_quantity_total
        GST = item.product.price_and_quantity_total * 0.06
    final_price= delhivery_charge + total + GST
    
    address = Customer.objects.filter(user=request.user)

    return render(request, 'app/checkout.html', {'cart_items': cart_items,'total':total,'final_price':final_price,'address':address})

#===================================== Payment ============================================

def payment(request):

    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')  # This will fetch value from radio button in which selected_addres contains value {{add.id}}, which will fetch value of customer id


    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total =0
    delhivery_charge =50
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price= delhivery_charge + total
    
    address = Customer.objects.filter(user=request.user)

    #================= Paypal Code ======================================
    
    host = request.get_host()   # Will fecth the domain site is currently hosted on.
    
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': final_price,
        'item_name': 'Pet',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('paymentsuccess', args=[selected_address_id])}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    #==========================================================================================================
    return render(request, 'app/payment.html', {'cart_items': cart_items,'total':total,'final_price':final_price,'address':address,'paypal':paypal_payment})

#===================================== Payment Success ============================================

def payment_success(request,selected_address_id):
    print('payment sucess',selected_address_id)   
    user =request.user
    customer_data = Customer.objects.get(pk=selected_address_id,)
    cart = Cart.objects.filter(user=user)
    total = 0
    for c in cart:
        c.product.price_and_quantity_total = (c.product.discounted_price * c.quantity) 
        total += c.product.price_and_quantity_total
        # GST = c.product.price_and_quantity_total * 0.06
    final_price= 50 + total + (c.product.price_and_quantity_total * 0.06)
    Order(user=user,customer=customer_data,grocery_product=c.product,quantity=c.quantity,total_price=final_price).save()
    c.delete()
    return render(request,'app/payment_success.html')


#===================================== Payment Failed ============================================


def payment_failed(request):
    return render(request,'app/payment_failed.html')

#===================================== Order ====================================================

def order(request):
    ord=Order.objects.filter(user=request.user)
    return render(request,'app/order.html',{'ord':ord})

#========================================== Buy Now ========================================================
def buynow(request,id):
    grocery = Grocery.objects.get(pk=id)     # cart_items will fetch product of current user, and show product available in the cart of the current user.
    delhivery_charge =50
    GST = (grocery.discounted_price * 0.06)
    final_price= delhivery_charge + grocery.discounted_price + GST
    
    address = Customer.objects.filter(user=request.user)

    return render(request, 'app/buynow.html', {'final_price':final_price,'address':address,'grocery':grocery})


def buynow_payment(request,id):

    if request.method == 'POST':
        selected_address_id = request.POST.get('buynow_selected_address')

    pet = Grocery.objects.get(pk=id)     # cart_items will fetch product of current user, and show product available in the cart of the current user.
    delhivery_charge =2000
    final_price= delhivery_charge + pet.discounted_price
    
    address = Customer.objects.filter(user=request.user)
    #================= Paypal Code ======================================

    host = request.get_host()   # Will fecth the domain site is currently hosted on.

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': final_price,
        'item_name': 'Pet',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('buynowpaymentsuccess', args=[selected_address_id,id])}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    #========================================================================

    return render(request, 'app/payment.html', {'final_price':final_price,'address':address,'pet':pet,'paypal':paypal_payment})

def buynow_payment_success(request,selected_address_id,id):
    print('payment sucess',selected_address_id)   # we have fetch this id from return_url': f"http://{host}{reverse('paymentsuccess', args=[selected_address_id])}
                                                  # This id contain address detail of particular customer
    user =request.user
    customer_data = Customer.objects.get(pk=selected_address_id,)
    
    pet = Grocery.objects.get(pk=id)
    Order(user=user,customer=customer_data,pet=pet,quantity=1).save()
   
    return render(request,'app/buynow_payment_success.html')
