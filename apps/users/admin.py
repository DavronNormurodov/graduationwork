from django.contrib import admin
from .models import User, Admins
from orders.models import Order


class OrderInline(admin.TabularInline):
    model = Order


class UserAdmin(admin.ModelAdmin):
    inlines = [OrderInline, ]


admin.site.register(User, UserAdmin)
admin.site.register(Admins)
