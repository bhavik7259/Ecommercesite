from django.shortcuts import render,redirect, get_object_or_404,HttpResponseRedirect,reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.auth.models import auth,User
from .models import Product,Category,Cart,Orderitem
from django.views import View
from django.db.models import Q
from django.views.generic import ListView

# Create your views here.

def fun(request):
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()

    data = {}
    data['products'] = products
    data['categories'] = categories
    
    return render(request, 'front/first.html', data)

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"invalid Username And Password ")
            return redirect('login')

    else:    
        return render(request,'Login Page/login page.html')

def register(request):

    if request.method=='POST':
        first_name=request.POST['first name']
        last_name=request.POST['last name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['psw']
        password2=request.POST['psw-repeat']
        
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email already taken')
                return redirect('register')
            else:
                user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password1,email=email)
                user.save()
        else:
            messages.info(request,'password not matching')
            return redirect('register')
        return redirect('/')
    else:
        return render(request,'Registration Page/Registration.html')

def logout(request):
    auth.logout(request)
    return redirect("/")

def details(request,myid):
    product=Product.objects.filter(id=myid)

    return render(request,'detailspage.html',{'product':product[0]})

def add_cart(request):
    context={}
    prods=Cart.objects.filter(user__id=request.user.id,status=False)
    context['prods']=prods
    if request.user.is_authenticated:
        if request.method=="POST":
            proid = request.POST["proid"]
            qt = request.POST["qt"]
            is_exits = Cart.objects.filter(product__id=proid,user__id=request.user.id,status=False)
            if len(is_exits)>0:
                messages.info(request,"helooo")
            else:    
                product =get_object_or_404(Product,id=proid)
                usr = get_object_or_404(User,id=request.user.id)
                c = Cart(user=usr,product=product,quantity=qt)
                c.save()
    else:
        context["status"] = "Please Login First to View Your Cart"
        return redirect('login')
    return render(request,'cart/cart1.html',context)

def get_cart_data(request):
    prods = Cart.objects.filter(user__id=request.user.id,status=False)
    sale,total,quantity =0,0,0
    for i in prods:
        sale += float(i.product.price)*i.quantity
        total += float(i.product.price)*i.quantity
        quantity+= int(i.quantity)

    res = {
        "total":total,"offer":sale,"quan":quantity,
    }
    return JsonResponse(res)

def change_quan(request):
    if "quantity" in request.GET:
        cid = request.GET["cid"]
        qt = request.GET["quantity"]
        cart_obj = get_object_or_404(Cart,id=cid)
        cart_obj.quantity = qt
        cart_obj.save()
        return HttpResponse(cart_obj.quantity)
    
    if "delete_cart" in request.GET:
        id = request.GET["delete_cart"]
        cart_obj = get_object_or_404(Cart,id=id)
        cart_obj.delete()
        return HttpResponse(1)

def price_total(product  , quantity):
    return product.price * quantity(product , quantity)

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings 

def process_payment(request):
    items = Cart.objects.filter(user_id__id=request.user.id)
    products=""
    amt=0
    inv = "INV10001-"
    cart_ids = ""
    p_ids =""
    for j in items:
        products += str(j.product.product_name)+"\n"
        p_ids += str(j.product.id)+","
        amt += float(j.product.price)
        inv +=  str(j.id)
        cart_ids += str(j.id)+","
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(amt),
        'item_name': products,
        'invoice': inv,
        'notify_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format("127.0.0.1:8000",
                                              reverse('payment_cancelled')),
    }
    usr = User.objects.get(username=request.user.username)
    ord = Orderitem(user_id=usr,cart_id=cart_ids,pro_id=p_ids)
    ord.save()
    ord.invoice_id = str(ord.id)+inv
    ord.save()
    request.session["order_id"] = ord.id

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process_payment.html', {'form': form})

def payment_done(request):
    if "order_id" in request.session:
        order_id = request.session["order_id"]
        ord_obj = get_object_or_404(Orderitem,id=order_id)
        ord_obj.status=True
        ord_obj.save()
        
        for i in ord_obj.cart_id.split(",")[:-1]:
            cart_object = Cart.objects.get(id=i)
            cart_object.status=True
            cart_object.save()
    return render(request,"payment/payment_successful.html")

def payment_cancelled(request):
    return render(request,"payment/payment_unsuccessful.html")

def search(request):
    return render(request,"payment/payment_successful.html")

class SearchResultsView(ListView):
    model = Product
    template_name = 'search.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(
            Q(product_name__icontains=query) | Q(desc__icontains=query) 
        )
        return object_list



