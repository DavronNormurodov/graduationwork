from django.contrib import admin
from .models import Order, OrderProduct
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    fields = ['user', 'total_price', 'location', 'status',
              'shipping_type', 'address', 'broker', 'created_at']

    readonly_fields = ['created_at']

    # fieldsets = [('user info', {'fields': ['user__name', ]}), ]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
