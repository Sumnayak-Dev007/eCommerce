from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from .models import (
    Category,Product,Cart,
    Wishlist,Order,OrderItem,
    Profile
    
    )
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random
# Create your views here.


def index(request):
    category = Category.objects.filter(status=0)
    product = Product.objects.all()
    context = {
        'category':category,
        'product':product
    }
    return render(request,'index.html',context)

def categories(request):
    category = Category.objects.filter(status=0)
    context = {
        'category':category
    }
    return render(request,'pages/categories.html',context)



def categoryview(request,slug):
    if (Category.objects.filter(slug=slug,status=0)):
        product = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug)
        context = {
            'product':product,
            'category':category
        }
        if not product:
             messages.error(request,"Products for this Category are not available at this moment")

    else:
        messages.error(request,"No such Category Found")
        return redirect("categories")
    return render(request,'pages/categoryview.html',context)



def productview(request,catslug,prodslug):
    if (Category.objects.filter(slug=catslug,status=0)):
        if (Product.objects.filter(slug=prodslug,status=0)):
            product = Product.objects.filter(slug=prodslug).first()

            context = {
                'product':product
            }
        else:
            messages.error(request,"No Such Product Found")
            return redirect("categories")
    else:
        messages.error(request,"No such Category Found")
        return redirect("categories")
    return render(request,'pages/productview.html',context)



#**************************CART VIEWS LOGIC ***************************************************

def addTocart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            prod_check = Product.objects.get(id=prod_id)
            if (prod_check):
                if (Cart.objects.filter(user=request.user,Product_id=prod_id).exists()):
                    return JsonResponse({'status':"Product Already in Cart :D"})
                else:
                    prod_qty=int(request.POST.get('prod_qty'))
                    if prod_check.quantity>= prod_qty:
                        Cart.objects.create(user=request.user,Product_id=prod_id,product_qty=prod_qty)
                        return JsonResponse({'status':"Product Added To Cart"})
                    else:
                        return JsonResponse({'status':"Only "+str(prod_check.quantity)+" Available in Stock"})
            else:
                return JsonResponse({'status':"No Such Product Exist"})

        else:
            return JsonResponse({'status': "Login to Continue"})
    return redirect('/')


@login_required
def cartview(request):
    cart = Cart.objects.filter(user=request.user)
    context ={
        'cart':cart
    }
    return render(request,'pages/cart.html',context)


def updatecartqty(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user, Product_id=prod_id)):
            prod_qty = int(request.POST.get('prod_qty'))
            cart = Cart.objects.get(Product_id=prod_id, user=request.user)

            
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status':"Updated Successfully"})
    return redirect('/')



def deletecart(request):
    if request.method == "POST":
        prod_id=int(request.POST.get('product_id'))
        if (Cart.objects.filter(user=request.user,Product_id=prod_id)):
            cart = Cart.objects.get(user=request.user,Product_id=prod_id)
            cart.delete()
            return JsonResponse({'status':'Item Deleted Successfully'})
    

#*************************WISHLIST*********************************
def add_w_list(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = request.POST.get('prod_id')
        
            # Check if product exists
            if Product.objects.filter(id=prod_id).exists():
                # Check if the product is already in the wishlist
                if Wishlist.objects.filter(user=request.user, product_id=prod_id).exists():
                    return JsonResponse({'status': 'Product Already in Wishlist'})
                
                # Add product to the wishlist
                Wishlist.objects.create(user=request.user, product_id=prod_id)
                return JsonResponse({'status': 'Product Added to Wishlist'})
        else:
            return JsonResponse({'status':"Login to Continue...."})
    
    return redirect("/")



@login_required
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)

    return render(request,'pages/wishlist.html',{'wishlist':wishlist})





def removewish(request):
    if request.method == "POST":
        prod_id = request.POST.get('prod_id')
        
        # Check if the product is in the user's wishlist
        wish = Wishlist.objects.filter(user=request.user, product_id=prod_id).first()
        
        if wish:
            wish.delete()
            return JsonResponse({'status': "Product Deleted From Wishlist"})
        else:
            return JsonResponse({'status': "Product not found in Wishlist"}, status=404)
    
    return JsonResponse({'status': "Invalid request"}, status=400)


#************************* CHECKOUT *******************************************
@login_required
def checkout(request):
    cartitem = Cart.objects.filter(user = request.user)
    total_price = 0
    for item in cartitem:
        total_price = total_price + item.product_qty * item.Product.selling_price

    profile = Profile.objects.filter(user=request.user).first()

    context = {
        'cartitem':cartitem,
        'total_price':total_price,
        'profile':profile
    }
    return render(request,'pages/checkout.html',context)


@login_required
def placeorder(request):
    if request.method == "POST":
        print("🔍 Received POST Data:", request.POST)
        
        currentuser = User.objects.filter(id=request.user.id).first()
        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('first_name')
            currentuser.last_name = request.POST.get('last_name')
            currentuser.email = request.POST.get('email')
            currentuser.save()

        if not Profile.objects.filter(user = request.user).first():
            profile = Profile()
            profile.user = request.user
            profile.phone = request.POST.get('phone')
            profile.address = request.POST.get('address')
            profile.city = request.POST.get('city')
            profile.state = request.POST.get('state')
            profile.country = request.POST.get('country')
            profile.pincode = request.POST.get('pincode')
            profile.save()

        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('first_name')
        neworder.lname = request.POST.get('last_name')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')
        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')


        cart = Cart.objects.filter(user=request.user)
        total_price = 0
        for item in cart:
            total_price += item.product_qty*item.Product.selling_price

        neworder.total_price = total_price

        track = "pay"+str(random.randint(111111,9999999))
        while (Order.objects.filter(trackno=track).exists()):
            track = "pay"+str(random.randint(111111,9999999))
        
        neworder.trackno = track
        neworder.save()

        for item in cart:
            OrderItem.objects.create(
                order = neworder,
                product = item.Product,
                price = item.Product.selling_price,
                qty = item.product_qty
            )

            prod = Product.objects.filter(id=item.Product.id).first()
            prod.quantity = prod.quantity-item.product_qty
            prod.save()


        Cart.objects.filter(user=request.user).delete()
        messages.success(request,"Your Order has been Placed Successfully")

        payMode = request.POST.get('payment_mode')
        if (payMode == "Paid by Razorpay" or payMode == "Paid by Paypal" ):
            return JsonResponse({'status':"Your order has been placed successfully"})
        
        return render(request,'pages/checkout.html')
        

    return redirect('/')

#********SEND THE TOTAL AMOUNT TO PAY TO RAZORPAY INTERFACE ***************************
def get_amount(request):
    cart = Cart.objects.filter(user = request.user)
    total_price = 0
    for item in cart:
        total_price = total_price + item.Product.selling_price * item.product_qty

    return JsonResponse({
        'amount':total_price
    })

@login_required
def orderss(request):
    return render(request,'pages/order_success.html')

#**********SEARCH BAR LOGIC **************************
def search(request):
    products = Product.objects.filter(status=0).values_list('meta_keywords', flat=True)
    prodlist = list(products)
    if not prodlist:
        return JsonResponse({"message": "No products found"}, status=404)
    return JsonResponse(prodlist, safe=False)

def searchproducts(request):
    if request.method == 'POST':
        searchitemi = request.POST.get('searchitemi', '').strip()
        
        if not searchitemi:
            return redirect(request.META.get('HTTP_REFERER', '/'))

        print("Search Query:", searchitemi)

        # Search by name or meta_keywords
        product = Product.objects.filter(
            Q(name__icontains=searchitemi) | Q(meta_keywords__icontains=searchitemi)
        ).first()

        print("Product Found:", product)

        if product:
            return redirect(f'/categories_view/{product.category.slug}')
        else:
            messages.info(request, "No product matched your search")
            return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def orders(request):


    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    order_data = []
    for order in orders:
        first_item = OrderItem.objects.filter(order=order).first()  # Get first product in the order
        order_data.append({
            'order': order,
            'product_image': first_item.product.product_image.url if first_item and first_item.product.product_image else None
        })
    return render(request,'pages/order.html',{'order_data': order_data})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'pages/order_detail.html', {'order': order, 'order_items': order_items})