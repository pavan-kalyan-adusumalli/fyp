from django.db import models
from sortedm2m.fields import SortedManyToManyField
from datetime import date, timedelta

d = date.today()

states = (
    ('Not mentioned','Choose a state'),
    ('Andhra Pradesh', 'ANDHRA PRADESH'),
    ('Arunachal Pradesh', 'ARUNACHAL PRADESH'),
    ('Assam', 'ASSAM'),
    ('Bihar', 'BIHAR'),
    ('Chandigarh', 'CHANDIGARH'),
    ('Chhattisgarh', 'CHHATTISGARH'),
    ('Delhi', 'DELHI'),
    ('Goa', 'GOA'),
    ("Gujarat", 'GUJARAT'),
    ('Haryana', 'HARYANA'),
    ('Himachal Pradesh', 'HIMACHAL PRADESH'),
    ('Jammu & Kashmir', 'JAMMU & KASHMIR'),
    ('Jharkhand', 'JHARKHAND'),
    ('Karnataka', 'KARNATAKA'),
    ('Kerala', 'KERALA'),
    ('Madhya Pradesh', 'MADHYA PRADESH'),
    ('Maharastra', 'MAHARASTRA'),
    ('Manipur', 'MANIPUR'),
    ('Meghalaya', 'MEGHALAYA'),
    ('Mizoram', 'MIZORAM'),
    ('Nagaland', 'NAGALAND'),
    ('Odisha','ODISHA'),
    ('Punjab', 'PUNJAB'),
    ('Rajasthan', 'RAJASTHAN'),
    ('Sikkim', 'SIKKIM'),
    ('Tamil nadu', 'TAMIL NADU'),
    ("Telangana", 'TELANGANA'),
    ('Tripura', 'TRIPURA'),
    ('Uttar pradesh', 'UTTAR PRADESH'),
    ('Uttarakhand', 'UTTARAKHAND'),
    ('West bengal', 'WEST BENGAL')
)

addresstypes = (
    ('Home', 'Home'),
    ('Office/Commercial', 'Office/Commercial')
)

# Create your models here.
class ASusers(models.Model):
    username = models.CharField(max_length=80)
    # user picture will be provided by google in form of an URL
    # so we are using charfield to store it
    userpicture = models.CharField(max_length=1000, default="")

    def __str__(self):
        return(f"{self.username}")

class Shop(models.Model):
    owner = models.ForeignKey(ASusers, on_delete=models.CASCADE, related_name="usershop")
    shopname = models.CharField(max_length=30)
    passkey = models.CharField(max_length=20)
    verificationStatus = models.BooleanField(default=False)
    shoppicture = models.ImageField(upload_to='shopimages/' ,default='../static/black.png')
    coverpic = models.ImageField(default='../static/default.jpg', blank=True)
    description = models.CharField(max_length=1000 ,default='')
    location = models.CharField(max_length=20, default="")
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    date_created = models.CharField(max_length=15, default=d)
    portfolio = models.CharField(max_length=500, default='', blank=True)
    fblink = models.CharField(max_length=500, default='', blank=True)
    twitterlink = models.CharField(max_length=500, default='', blank=True)
    instalink = models.CharField(max_length=500, default='', blank=True)
    maplink = models.CharField(max_length=1000, default="", blank=True)

    def __str__(self):
        return(f"{self.shopname}")

class Product(models.Model):
    productname = models.CharField(max_length=40)
    soldby = models.CharField(max_length=20, default="Not Available")
    actualPrice = models.IntegerField()
    discountedPrice = models.IntegerField()
    producttype = models.CharField(max_length=15)
    material = models.CharField(max_length=15)
    quantity = models.IntegerField()
    warranty = models.IntegerField()
    countryoforigin = models.CharField(max_length=15)
    description = models.CharField(max_length=200, default="Not Available")
    uploadedshop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")
    onestar = models.IntegerField(default=0)
    twostar = models.IntegerField(default=0)
    threestar = models.IntegerField(default=0)
    fourstar = models.IntegerField(default=0)
    fivestar = models.IntegerField(default=0)
    image1 = models.ImageField(upload_to="productImages/")
    image2 = models.ImageField(upload_to="productImages/")
    image3 = models.ImageField(upload_to="productImages/", null=True)
    image4 = models.ImageField(upload_to="productImages/", null=True)
    featuredProduct = models.BooleanField(default=False)
    average_rating = models.IntegerField(default=0)

    def __str__(self):
        return(f"id:{self.id} {self.productname}")

class Cart(models.Model):
    cartowner = models.ForeignKey(ASusers, on_delete=models.CASCADE, related_name="cartowner")
    products = SortedManyToManyField(Product, blank=True, related_name="productsincart")


class ProductCategory(models.Model):
    productcategoryname = models.CharField(max_length=30)
    owner = models.ForeignKey(ASusers, on_delete=models.CASCADE, related_name='categories')
    shopname = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shopproductcategories', blank=True, null=True)
    productname = SortedManyToManyField(Product, blank=True, related_name='productcategories')

class Address(models.Model):
    address_owner = models.ForeignKey(ASusers, on_delete=models.CASCADE, related_name="useraddress")
    fullname = models.CharField(max_length=35)
    mobilenumber = models.CharField(max_length=15)
    pincode = models.CharField(max_length=10)
    house_no = models.CharField(max_length=20)
    area = models.CharField(max_length=30)
    landmark = models.CharField(max_length=40)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20, choices=states)
    country = models.CharField(max_length=10)
    addresstype = models.CharField(max_length=30, choices=addresstypes)

    def __str__(self):
        return (f"{self.fullname}, {self.house_no}, {self.area}, {self.landmark}, {self.city}, {self.state}, {self.country}, {self.pincode}.")

class Orders(models.Model):
    razorpay_orderid = models.CharField(max_length=50, default="undefined")
    transactionid = models.CharField(max_length=50, default="undefined")
    signature = models.CharField(max_length=75, default="undefined")
    orderby = models.ForeignKey(ASusers, on_delete=models.CASCADE, related_name="userorders")
    ordered_products = SortedManyToManyField(Product, related_name="orderedproducts", help_text="Note: Reference field only, You won't get extra money for selecting products other than customer selected ones!")
    payment_status = models.BooleanField(default=False)
    delivary_status = models.BooleanField(default=False, help_text="Mark this once order has been delivered.")
    date = models.CharField(max_length=20)
    expecteddate = models.CharField(max_length=20, default="")
    rating = models.IntegerField(default=0)
    shippingAddress = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="useraddress", help_text="Shipping address for reference.")
    orderstatus = models.CharField(max_length=100, default="Order Placed", help_text="Help customer to track orderby entering tracking status.")
    ordertotal = models.IntegerField(default=0)

    def __str__(self):
        return (f"Order ID {self.id}")

class Comment(models.Model):
    commentator = models.ForeignKey(ASusers, on_delete=models.CASCADE, related_name="usercomments")
    comment = models.CharField(max_length=500, default='')
    commented_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="productcomments")
    date = models.CharField(max_length=20)

class Rating(models.Model):
    rated_by = models.ForeignKey(ASusers, on_delete=models.CASCADE, related_name="userratings")
    rating = models.IntegerField(default=0)
    rated_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="productratings")
    date = models.CharField(max_length=20)
