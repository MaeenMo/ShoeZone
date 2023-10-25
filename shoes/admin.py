from django.contrib import admin
from django.contrib.admin.models import *
from .models import *


class ShoeAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'price']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        LogEntry.objects.all().delete()
        count = int(Shoe.objects.count())
        arr = [1 for i in range(count)]
        for i in range(1, count):
            arr[i] = arr[i - 1] + 1
        y = 0
        for i in Shoe.objects.all():
            i.shoe_num = arr[y]
            i.save()
            y += 1
        return super().change_view(request, object_id, form_url, extra_context)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        fields.remove('shoe_num')
        # Check if the current user is an admin
        if request.user.username == 'admin':
            fields.remove('img')
            fields.remove('color_hexa')
            fields.remove('shoe_num')
            return fields

        # For regular users, show all fields
        return fields


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'user_ordered', 'total_price', 'created_at']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        LogEntry.objects.all().delete()
        return super().change_view(request, object_id, form_url, extra_context)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        # fields.remove('shoe_num')
        # Check if the current user is an admin
        if request.user.username == 'admin':
            fields.remove('img')
            fields.remove('color_hexa')
            fields.remove('shoe_num')
            return fields

        # For regular users, show all fields
        return fields

class Cart_itemAdmin(admin.ModelAdmin):
    list_display = ['owner', 'product', 'product_qty', 'selected_size', 'created_at']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        LogEntry.objects.all().delete()
        return super().change_view(request, object_id, form_url, extra_context)


admin.site.register(Shoe, ShoeAdmin)
admin.site.register(Cart_item)
admin.site.register(Order, OrderAdmin)
