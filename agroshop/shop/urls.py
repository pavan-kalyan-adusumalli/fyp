from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="homepage"),
    path("location", views.locationSearch, name="locationsearch"),
    path("viewproduct/pid=<int:pid>", views.viewProduct, name="viewproduct"),
    path("accounts/profile/", views.profile),

    path("createshop", views.createShop, name="createshop"),
    path("new_shop_setup", views.setupShop, name="setupshop"),
    path("myshop", views.myshop, name="myshop"),
    path("addproduct", views.addproduct, name="addproduct"),
    path("uploadproduct", views.uploadedproduct, name="uploadproduct"),
    path("viewshop/shopid=<int:sid>", views.viewshop, name="viewshop"),
    path("cart", views.addToCart, name="viewcart"),
    path("cart/pid=<int:pid>", views.addToCart, name="addtocart"),
    path("removefromcart/pid=<int:pid>", views.removefromcart, name="removefromcart"),

    
    path("selectaddress/cartid=<int:cartid>", views.selectaddress, name="selectaddressforcart"),
    path("selectaddress/prodid=<int:prodid>", views.selectaddress, name="selectaddressforprod"),

    # path("checkout", views.checkout, name="checkout"),
    path("checkout/pid=<int:pid>", views.checkout, name="checkoutproduct"),
    path("checkout/cartid=<int:cartid>", views.checkout, name="checkoutcart"),
    path("paymentstatus", views.paystatus, name="paystatus"),
    path("paymentstatus/status=<str:status>", views.paymentstatus, name="paymentstatus"),

    path("qrsavedetails", views.qrsavedetails, name="qrsavedetails"),

    path("myorders", views.myorders, name="myorders"),
    path("customize/<int:shopid>", views.customize, name="customize"),
    path("submitcomment", views.submitcomment, name="submitcomment"),
    path("submitrating", views.submitrating, name="submitrating"),
    path("shopsaroundyou", views.shopsAroundYou, name="shopsaroundyou"),
    path("displaymap/shopid=<int:shopid>", views.displaymap, name="displaymap"),
    path("searchforproduct", views.searchforproduct),
    path("search_results", views.search, name='searchsomething'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)