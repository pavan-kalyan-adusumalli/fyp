from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ASusers)
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Orders)
admin.site.register(Comment)
admin.site.register(Rating)

class ShopAdminArea(admin.AdminSite):
    site_header = "Shop Admin Area"

class ShopAdminPermissions(admin.ModelAdmin):

    # fields = ['ordered_products', "delivary_status", 'shippingAddress', "orderstatus"]
    fieldsets = (
        ('Read Only Section',{
            'fields':('payment_status', 'ordered_products', 'shippingAddress',),
            'description' : "Do not try to change fields under this section",
            'classes':("collapse",),
        }),
        ('Writable Section',{
            'fields':('delivary_status', 'orderstatus'),
        }),
    )

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return obj is None or obj.payment_status
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_view_permission(self, request, obj=None):
        return True

shop_admin = ShopAdminArea(name="ShopAdmin")

shop_admin.register(Orders, ShopAdminPermissions)