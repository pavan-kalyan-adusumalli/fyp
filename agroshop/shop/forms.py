from django import forms
from .models import Shop, Product, Address
class AddShopForm(forms.ModelForm):
    passkey = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea, max_length=1000)
    portfolio = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'aria-describedby':'basic-addon1'}))
    fblink = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'aria-describedby':'basic-addon1'}))
    twitterlink = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'aria-describedby':'basic-addon1'}))
    instalink = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'aria-describedby':'basic-addon1'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    longitude = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    latitude = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    maplink = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter map URL'}))
    class Meta:
        model = Shop
        fields = ['owner', 'shopname', 'shoppicture', 'passkey', 'description', 'location', 'latitude', 'longitude', 'portfolio', 'fblink', 'twitterlink', 'instalink', 'maplink']

class AddProductForm(forms.ModelForm):
    productname = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class':'form-control' ,'placeholder':'Add a title that describes your product'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Tell viewers about the product'}))
    actualPrice = forms.IntegerField()
    discountedPrice = forms.IntegerField()
    producttype = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' ,'placeholder':'Mention type of the product'}))
    material = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' ,'placeholder':'Material used for manufacturing product'}))
    quantity = forms.IntegerField()
    warranty = forms.IntegerField()
    countryoforigin = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' ,'placeholder':'Country of Manufacturing'}))
    soldby = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' ,'placeholder':"Product's manufacturer name"}))
    class Meta:
        model = Product
        fields = ['productname',"description", 'soldby', 'actualPrice', 'discountedPrice', 'producttype', 'material', 'quantity', 'warranty','countryoforigin', 'uploadedshop', 'image1', 'image2', 'image3', 'image4', 'featuredProduct']

class AddAddressForm(forms.ModelForm):
    fullname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your Full Name goes here'}))
    mobilenumber = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'Placeholder':"Mobile number"}))
    pincode = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'Placeholder':"6 digits [0-9] PIN code"}))
    house_no = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'Placeholder':""}))
    area = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'Placeholder':""}))
    landmark = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'Placeholder':"E.g. near apollo hospital"}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'Placeholder':""}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'Placeholder':""}))

    class Meta:
        model = Address
        fields = ['address_owner', 'fullname', 'mobilenumber', 'pincode', 'house_no', 'area', 'landmark', 'city', 'state', 'country', 'addresstype']