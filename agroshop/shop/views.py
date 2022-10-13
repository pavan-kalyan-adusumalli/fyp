from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from .models import *
from .forms import AddShopForm, AddProductForm, AddAddressForm
from django.contrib.auth.hashers import make_password
from agroshop.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import re

# Create your views here.
def index(request):
    products = Product.objects.all()
    if(request.user.is_authenticated):
        userobjects = ASusers.objects.all()
        userslist = [user.username for user in userobjects]

        social_info = SocialAccount.objects.filter(user=request.user)
        userpic = social_info[0].extra_data['picture']

        print(request.user.username)
        
        if(request.user.username not in userslist):
            #create a new user if he is loggin for the first time
            newuser = ASusers(username=request.user, userpicture=userpic)
            newuser.save()
        cur_user_obj = ASusers.objects.get(username=request.user.username)
        user_shop = cur_user_obj.usershop.all().first()
        user_cart = cur_user_obj.cartowner.all().first()
        if(not user_cart):
            cart = Cart(cartowner = cur_user_obj)
            cart.save()
        
        return render(request, "shop/index.html", {"extradata":social_info[0].extra_data, 'usershop':user_shop, 'products':products[::-1]})
    return render(request, "shop/index.html", {"products":products[::-1]})

def createShop(request):
    if(request.user.is_authenticated):
        social_info = SocialAccount.objects.filter(user=request.user)
        return render(request, 'shop/createShop.html', {'extradata':social_info[0].extra_data})

def setupShop(request):
    #get the post data
    shopname = request.POST.get('customShopName')
    user = ASusers.objects.filter(username=request.user.username).first()
    if(request.user.is_authenticated):
        social_info = SocialAccount.objects.filter(user=request.user)
        form = AddShopForm()
        if(shopname):
            return render(request, 'shop/setupshop.html', {'extradata':social_info[0].extra_data, 'form':form, 'ShopName':shopname, 'curuser':user})
        return render(request, 'shop/setupshop.html', {'extradata':social_info[0].extra_data, 'form':form, 'ShopName':social_info[0].extra_data.get('name'), 'curuser':user})

def myshop(request):
    if(not request.user.is_authenticated):
        return(render(request, "shop/error.html", {'message':'You should signin to see this', 'info':'Refresh and Use signin Button to login'}))
    if(request.method == 'POST'):
        shopname = request.POST.get('shopname')
        #print(request.POST.get('shoppicture'))
        form = AddShopForm(request.POST, request.FILES)
        print(form.errors)
        # print(form.cleaned_data['passkey'])

        if(form.is_valid()):
            form.save()
        
    social_info = SocialAccount.objects.filter(user=request.user)
    cur_user_obj = ASusers.objects.filter(username=request.user.username).first()
    cur_shop_obj = cur_user_obj.usershop.all().first()
    verificationStatus = cur_shop_obj.verificationStatus
    print(cur_shop_obj.shoppicture.url)
    shop_products = cur_shop_obj.products.all()
    featuredproducts = [prod for prod in shop_products if prod.featuredProduct==True]
    # print(featuredproducts)
    total_products = len(shop_products)
    return render(request, 'shop/myshop.html', {'customizing':True, 'verefied': verificationStatus, 'extradata': social_info[0].extra_data, 'usershop':cur_shop_obj, 'shopProducts':shop_products, 'featuredproducts':featuredproducts, 'totalproducts':total_products})

def viewshop(request, sid):
    if(not request.user.is_authenticated):
        return(render(request, "shop/error.html", {'message':'You should signin to see this', 'info':'Refresh and Use signin Button to login'}))
    
    social_info = SocialAccount.objects.filter(user=request.user)
    cur_user_obj = ASusers.objects.filter(username=request.user.username).first()
    cur_shop_obj = Shop.objects.filter(id=sid).first()
    verificationStatus = cur_shop_obj.verificationStatus
    shop_products = cur_shop_obj.products.all()
    featuredproducts = [prod for prod in shop_products if prod.featuredProduct==True]
    total_products = len(shop_products)
    return render(request, 'shop/viewshop.html', {'verefied': verificationStatus, 'extradata': social_info[0].extra_data, 'usershop':cur_shop_obj, 'shopProducts':shop_products, 'featuredproducts':featuredproducts, 'totalproducts':total_products})

def addproduct(request):
    if(request.user.is_authenticated):
        social_info = SocialAccount.objects.filter(user=request.user)
        form = AddProductForm()
        cur_user_obj = ASusers.objects.filter(username=request.user.username).first()
        shop = cur_user_obj.usershop.all().first()
        #print(channel)
        if(shop is None):
            return render(request, 'shop/error.html', {'message': 'You need to create a shop to add product.'})
        return render(request, 'shop/addproduct.html', {'extradata':social_info[0].extra_data, 'productform':form, 'shop':shop, 'usershop':shop})
    return render(request, 'shop/error.html', {'message':'You should signin to see this', 'info':'Use signin Button to login'})

def uploadedproduct(request):
    if(request.method=='POST'):
        form = AddProductForm(request.POST, request.FILES)
        
        if(form.is_valid()):
            #print('form is valid')
            form.save()
            #if there is any playlist save product to playlist here
            return HttpResponseRedirect(reverse('homepage'))
        # print(form.data)
        print(form['actualprice'])
        print(form.errors)
        return HttpResponse('Invalid form, Please Try Again!')

def profile(request):
    return HttpResponseRedirect(reverse("homepage"))

def locationSearch(request):
    return render(request, "shop/locationsearch.html")


def shopsAroundYou(request):
    location = request.POST.get("locationname")
    
    shops = None
    # case insensitive query
    shops = Shop.objects.filter(location__iexact = location).all()
    
    if(request.user.is_authenticated):
        social_info = SocialAccount.objects.filter(user=request.user)
        cur_user_obj = ASusers.objects.get(username=request.user.username)
        user_shop = cur_user_obj.usershop.all().first()
        return render(request, "shop/locationresults.html", {'extradata':social_info[0].extra_data, 'usershop':user_shop, "shops":shops })
    return render(request, "shop/locationresults.html", {"shops":shops})


def viewProduct(request, pid):
    product_obj = Product.objects.get(id=pid)
    prod_shop_obj = product_obj.uploadedshop
    total_shop_products = len(prod_shop_obj.products.all())
    product_comments = product_obj.productcomments.all()

    oneStar = product_obj.onestar
    twoStar = product_obj.twostar
    threeStar = product_obj.threestar
    fourStar = product_obj.fourstar
    fiveStar = product_obj.fivestar

    stardict = {"onestar":oneStar, "twostar":twoStar, "threestar":threeStar, "fourstar":fourStar, "fivestar":fiveStar}

    # no of total ratings for product
    total_ratings = oneStar + twoStar + threeStar + fourStar + fiveStar
    #sum of all stars for product
    total = 1*oneStar + 2*twoStar + 3*threeStar + 4*fourStar + 5*fiveStar

    if(total_ratings != 0):
        # total_ratings_avg = total / total_ratings
    
        onestarper = int((oneStar/total_ratings)*100)
        twostarper = int((twoStar/total_ratings)*100)
        threestarper = int((threeStar/total_ratings)*100)
        fourstarper = int((fourStar/total_ratings)*100)
        fivestarper = int((fiveStar/total_ratings)*100)
    else:
        total_ratings_avg = onestarper = twostarper = threestarper = fourstarper = fivestarper = 0
    
    total_ratings_avg = product_obj.average_rating

    starPerDict = {"onestarper":onestarper, "twostarper":twostarper, "threestarper":threestarper, "fourstarper":fourstarper, "fivestarper":fivestarper}
    fill_stars = range(int(total_ratings_avg))
    empty_stars = range(int(5-total_ratings_avg))
    print(total_ratings)

    if(request.user.is_authenticated):
        social_info = SocialAccount.objects.filter(user=request.user)
        cur_user_obj = ASusers.objects.get(username=request.user.username)
        user_shop = cur_user_obj.usershop.all().first()
        
        #checking if the product is in cart or not
        product_in_cart = False
        user_cart_obj = cur_user_obj.cartowner.first()
        if(user_cart_obj and product_obj in user_cart_obj.products.all()):
            product_in_cart = True
        # end of check


        return render(request, "shop/viewproduct.html", {'extradata':social_info[0].extra_data, 'usershop':user_shop, 'product':product_obj, 'totalproducts':total_shop_products, 'productshop':prod_shop_obj, 'incart':product_in_cart, "totalratings":total_ratings, "stardict":stardict, "starperdict":starPerDict, 'average':total_ratings_avg, "comments": product_comments, 'fillstars':fill_stars, 'emptystars':empty_stars})
    return render(request, "shop/viewproduct.html", {'product':product_obj, 'totalproducts':total_shop_products, 'productshop':prod_shop_obj, 'incart':False, "totalratings":total_ratings, "stardict":stardict, "starperdict":starPerDict, 'average':total_ratings_avg, "comments": product_comments, 'fillstars':fill_stars, 'emptystars':empty_stars})
def addToCart(request, pid=0):
    if(not request.user.is_authenticated):
        return render(request, "shop/error.html", {"message":'You should login to use this feature'})
    owner_obj = ASusers.objects.filter(username=request.user.username).first()
    social_info = SocialAccount.objects.filter(user=request.user)
    user_shop = owner_obj.usershop.all().first()
    relatedproducts = Product.objects.all()[:3]
    cart_obj = owner_obj.cartowner.first()
    if(pid):
        product_id = pid
        product_obj = Product.objects.filter(id=product_id).first()
        # if owner does not have cart object, create one
        if(not cart_obj):
            cart_obj = Cart(cartowner=owner_obj)
            cart_obj.save()
            cart_obj.products.add(product_obj)
        else:
            #if owner is having cart
            if(product_obj in cart_obj.products.all()):
                pass
            else:
                cart_obj.products.add(product_obj)
        cart_products = cart_obj.products.all()
        print(product_obj, owner_obj, cart_obj)
        subtotal = 0
        for product in cart_products:
            subtotal += product.discountedPrice
        print(subtotal)
        return render(request, "shop/cart.html", {"cartproducts":cart_products, "subtotal":subtotal, "noofitems":len(cart_products), "cartobj":cart_obj, 'extradata':social_info[0].extra_data, 'usershop':user_shop, "relatedproducts":relatedproducts})
    else:
        cart_products = cart_obj.products.all()
        subtotal = 0
        for product in cart_products:
            subtotal += product.discountedPrice
        print(subtotal)
        
        return render(request, "shop/cart.html", {"cartproducts":cart_products, "subtotal":subtotal, "noofitems":len(cart_products), "cartobj":cart_obj, 'extradata':social_info[0].extra_data, 'usershop':user_shop, "relatedproducts":relatedproducts})

def removefromcart(request, pid):
    cur_user_obj = ASusers.objects.filter(username=request.user.username).first()
    product_obj = Product.objects.filter(id=pid).first()
    cart_obj = cur_user_obj.cartowner.first()

    cart_obj.products.remove(product_obj)
    cart_obj.save()
    return HttpResponseRedirect(reverse("viewcart"))

def selectaddress(request, cartid=0, prodid=0):
    cart_obj = None
    if(cartid):
        cart_obj = Cart.objects.filter(id=cartid).first()
    if(prodid):
        prod_obj = Product.objects.filter(id=prodid).first()
    cur_user_obj = ASusers.objects.filter(username=request.user.username).first()
    if(request.user.is_authenticated):
        if(request.method=='POST'):
            # get user's previous orders
            # last_order_obj = Orders.objects.filter(orderby = cur_user_obj).last()
            # then get address from last order
            # if order is none
            # if(last_order_obj is None):
            # create new order with address
            # existing_address = Address.objects.filter(address_owner = cur_user_obj).first()
            # everytime after adding new address, deleting previous address
            # if(existing_address is not None):
                # existing_address.delete()
            # print(existing_address)

            form = AddAddressForm(request.POST, request.FILES)
            print(form.data)
            print(form.errors)

            if(form.is_valid()):
                form.save()
            #after saving address redirect user to checkout
            if(cart_obj):
                return HttpResponseRedirect(reverse("checkoutcart", args=[cartid]))
            return HttpResponseRedirect(reverse("checkoutproduct", args=[prodid]))
        else:
            # displaying previously saved address from orders (if any) along with new address form
            # existing_address = Address.objects.filter(address_owner = cur_user_obj).first()
            last_order_obj = Orders.objects.filter(orderby = cur_user_obj).last()
            existing_address = None
            if(last_order_obj):
                existing_address = last_order_obj.shippingAddress


            form = AddAddressForm()
            if(cart_obj):
                return render(request, "shop/addaddress.html", {'form':form, "savedadd":existing_address, 'userobj':cur_user_obj, "cartobj":cart_obj, "iscart":True})
            return render(request, "shop/addaddress.html", {'form':form, "savedadd":existing_address, 'userobj':cur_user_obj, "prodobj":prod_obj, "iscart":False})
        
    else:
        return render(request, "shop/error.html", {'message':'You should login to see this', 'info':'Refresh page and Use signin Button to login'})

client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))

def checkout(request, pid=0, cartid=0):
    if(not request.user.is_authenticated):
        return render(request, "shop/error.html", {'message':'You should login to see this', 'info':'Refresh page and Use signin Button to login'})
    
    owner_obj = ASusers.objects.filter(username=request.user.username).first()
    prod_obj, cart_obj = None, None
    order_products = []
    user_cart = Cart.objects.filter(cartowner = owner_obj).first()
    if(pid):
        prod_obj = Product.objects.filter(id=pid).first()
        order_products.append(prod_obj)
        # removing product from user cart once buyed
        user_cart.products.remove(prod_obj)
        user_cart.save()
    
    if(cartid):
        cart_obj = Cart.objects.filter(id=cartid).first()
        order_products = cart_obj.products.all()
        # removing product from user cart once buyed
        for product in order_products:
            print("removing")
            user_cart.products.remove(product)
            user_cart.save()
    

    total_amount = 0
    for i in order_products:
        total_amount += i.discountedPrice
    print(total_amount)

    order_currency = 'INR'
    payment_order = client.order.create(dict(amount=total_amount*100, currency = order_currency, payment_capture=1))
    payment_order_id = payment_order['id']
    print(payment_order_id)
    order_status = payment_order['status']
    print(order_status)
    
    
    context = {
        'amount':total_amount, 'api_key':RAZORPAY_API_KEY, 'order_id':payment_order_id,
        'orderproducts':order_products
    }
    #saving orderid, transaction id
    d = date.today()
    delivarydate = d + timedelta(days=10)
    cur_user_obj = ASusers.objects.filter(username=request.user.username).first()
    address = Address.objects.filter(address_owner = cur_user_obj).last()
    order = Orders(orderby = cur_user_obj, date = d, expecteddate = delivarydate ,razorpay_orderid = payment_order_id, shippingAddress = address, ordertotal=total_amount)
    order.save()
    for prod in order_products:
        order.ordered_products.add(prod)
        order.save()
    return render(request, "shop/checkout.html", context)

@csrf_exempt
def paystatus(request):
    if(request.method=="POST"):
        print(request.POST.get("error"))
        print(request.POST.get("razorpay_payment_id"))
        print(request.POST.get("razorpay_order_id"))
        print(request.POST.get("razorpay_signature"))
        payment_id = request.POST.get("razorpay_payment_id")
        ordid = request.POST.get("razorpay_order_id")
        sig = request.POST.get("razorpay_signature")

        if(ordid):
            order = Orders.objects.filter(razorpay_orderid = ordid).first()
            print(order.razorpay_orderid)
            order.transactionid = payment_id
            order.signature = sig
            order.payment_status = True
            order.save()

    if(payment_id):
        return render(request, "shop/paymentstatus.html", {"paymentstatus":True})
    else:
        return render(request, "shop/paymentstatus.html", {"paymentstatus":False})


@csrf_exempt
def paymentstatus(request, status):
    pay_status = False
    if(status=='success'):
        pay_status = True
    return render(request, "shop/paymentstatus.html", {"paymentstatus":pay_status})

def qrsavedetails(request):
    if(request.user.is_authenticated):
        ordid = request.GET.get("ordid")
        payid = request.GET.get("payid")
        sig = request.GET.get("sig")

        print(ordid, payid, sig, sep="\n")

        order = Orders.objects.filter(razorpay_orderid = ordid).first()
        order.transactionid = payid
        order.signature = sig
        order.payment_status = True
        order.save()

        cur_user_obj = ASusers.objects.filter(username=request.user.username).first()
        
        #Save order
        d=date.today()
        # order = Orders(razorpay_order_id = ordid, transactionid = payid, signature = sig, orderby = cur_user_obj)
        return JsonResponse({'commentStatus':'true'})
    else:
        return JsonResponse({"commentStatus":'loggedout'})

def myorders(request):
    if(request.user.is_authenticated):
        cur_user_obj = ASusers.objects.filter(username = request.user.username).first()
        order_objs = cur_user_obj.userorders.all()
        print(order_objs)
        return render(request, "shop/myorders.html", {"orderobjects":order_objs[::-1]})
    else:
        return(render(request, "shop/error.html", {'message':'You should signin to see this', 'info':'Refresh and Use signin Button to login'}))

def customize(request, shopid):
    if(request.user.is_authenticated):
        shop_obj = Shop.objects.get(id=shopid)
        if(request.method == 'POST'):
            print("in post")
            #shoppic = request.POST.get('shoppicture')
            #coverpic = request.POST.get('coverpic')
            desc = request.POST.get('description')    
            form = AddShopForm(request.POST, request.FILES, instance=shop_obj)
            if(form.is_valid):
                #print(form.data)
                form.save()
                #print(request.FILES)
            return HttpResponseRedirect(reverse('myshop'))
        else:
            print("in get")
            user = ASusers.objects.filter(username=request.user.username).first()
            social_info = SocialAccount.objects.filter(user=request.user)
            
            shopname = shop_obj.shopname
            print(shopname)
            form = AddShopForm(instance = shop_obj)
            if(shopname):
                return render(request, 'shop/setupshop.html', {'customizing':True, 'extradata':social_info[0].extra_data, 'form':form, 'ShopName':shopname, 'shopobj':shop_obj, 'curuser':user})
            #return render(request, 'videos/channelsetup.html', {'extradata':social_info[0].extra_data, 'form':form, 'ChannelName':social_info[0].extra_data.get('name'), 'curuser':user})
    else:
        return render(request, 'shop/error.html', {'message':'You should log in to see this'})

def submitcomment(request):
    if(request.user.is_authenticated):
        # print("hai")
        pid = int(request.GET.get('prodid'))
        user = ASusers.objects.filter(username=request.user.username).first()
        prod = Product.objects.filter(id=pid).first()

        #create comment and save
        comment = request.GET.get("content")
        print("comment", comment)
        d = date.today()
        cmnt = Comment(comment = comment, commentator=user, commented_product=prod, date=d)
        cmnt.save()
        return JsonResponse({'commentStatus':'true'})
    else:
        return JsonResponse({"commentStatus":'loggedout'})

def submitrating(request):
    if(request.user.is_authenticated):
        pid = int(request.GET.get('prodid'))
        print(pid)
        user = ASusers.objects.filter(username=request.user.username).first()
        prod = Product.objects.filter(id=pid).first()
        print(prod)

        #get rating
        rating = request.GET.get("rating")
        criteria1 = Q(rated_by=user)
        criteria2 = Q(rated_product=prod)
        previous_rating = Rating.objects.filter(rated_product=prod, rated_by=user).first()
        print(previous_rating)
        # if there is any previous rating change it and save it with new rating
        if(previous_rating):
            return JsonResponse({"ratingstatus":str(previous_rating.rating)})
            #get previous rating number
            prev_rate_no = previous_rating.rating
            if(prev_rate_no == 1):
                prod.onestar = prod.onestar - 1
            elif(prev_rate_no == 2):
                prod.twostar = prod.twostar - 1
            elif(prev_rate_no == 3):
                prod.threestar = prod.threestar - 1
            elif(prev_rate_no == 4):
                prod.fourstar = prod.fourstar - 1
            elif(prev_rate_no == 5):
                prod.fivestar = prod.fivestar - 1
            prod.save()
            previous_rating.delete()
            previous_rating.save()
        
        #save rating on product object
        if(rating == '1'):
            prod.onestar = prod.onestar + 1
        if(rating == '2'):
            prod.twostar = prod.twostar + 1
        if(rating == '3'):
            prod.threestar = prod.threestar + 1
        if(rating == '4'):
            prod.fourstar = prod.fourstar + 1
        if(rating == '5'):
            prod.fivestar = prod.fivestar + 1
        prod.save()

        # updating average rating for product
        one = prod.onestar
        two = prod.twostar
        three = prod.threestar
        four = prod.fourstar
        five = prod.fivestar
        
        total_ratings = one + two + three + four + five
        
        total = 1*one + 2*two + 3*three + 4*four + 5*five
        print("total ratings", one , two , three , four , five)
        
        avg = total/total_ratings
        prod.average_rating = avg
        prod.save()

        d = date.today()
        rate = Rating(rating=rating, rated_by=user,rated_product=prod, date = d)
        rate.save()
        return JsonResponse({"ratingstatus":"true"})
    else:
        return JsonResponse({"ratingstatus":'loggedout'})

def displaymap(request, shopid):
    shopobj = Shop.objects.filter(id=shopid).first()
    if(request.user.is_authenticated):
        social_info = SocialAccount.objects.filter(user=request.user)
        cur_user_obj = ASusers.objects.get(username=request.user.username)
        user_shop = cur_user_obj.usershop.all().first()
        return render(request, "shop/displaymap.html", {'shop':shopobj, 'extradata':social_info[0].extra_data, 'usershop':user_shop})
    return render(request, "shop/displaymap.html", {"shop":shopobj})

def searchforproduct(request):
    text = request.GET.get('text')
    if(text):
        relatedlist = [i.productname for i in Product.objects.all() if re.search(f"\A{text.lower()}",i.productname.lower())]
        #print(relatedlist)
        print(relatedlist)
        return JsonResponse({"relatedresults":relatedlist})
    return JsonResponse({"relatedresults":'[]'})
    return HttpResponse(relatedlist)

def search(request):
    searchedText = request.POST.get('searchedtext')
    relatedproducts = list(Product.objects.filter(productname=searchedText))
    relatedshops = list(Shop.objects.filter(shopname=searchedText))
    print(searchedText)
    print(Product.objects.all())
    morerelatedproducts = [i for i in Product.objects.all() if i not in relatedproducts and searchedText.lower() in i.productname.lower()]
    morerelatedshops = [i for i in Shop.objects.all() if i not in relatedshops and searchedText.lower() in i.shopname.lower()]
    relatedproducts += morerelatedproducts
    relatedshops += morerelatedshops
    #print(relatedvideos)
    if(request.user.is_authenticated):
        cur_user_obj = ASusers.objects.filter(username=request.user.username).first()
        return render(request, 'shop/search.html', {'searchedtext':searchedText, 'products':relatedproducts, 'shops':relatedshops})
        
    return render(request, 'shop/search.html', {'searchedtext':searchedText, 'products':relatedproducts, 'shops':relatedshops})