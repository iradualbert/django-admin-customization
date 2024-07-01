from django.contrib import admin
from .models import Lead, Product, Customer, Order, Interaction
from django.utils.translation import ngettext
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse


# GLOBAL ACTIONS
def export_selected_objects(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response

admin.site.add_action(export_selected_objects)
admin.site.disable_action('delete_selected')    



@admin.action(description='Make selected products public')
def make_product_public(modeladmin, request, queryset):
    queryset.update(status='public')
    

@admin.action(description='Make selected products private') 
def make_product_private(modeladmin, request, queryset):
    queryset.update(status='private')


# @admin.action(description='Make selected orders completed')
# def make_order_completed(modeladmin, request, queryset):
#     queryset.update(status='completed')    


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('name', 'created_at',)  

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency', 'status', 'created_at')
    search_fields = ('name', )
    list_filter = ('name', 'created_at',)
    actions = [make_product_public, make_product_private, 'export_as_json']	
    
    def export_as_json(modeladmin, request, queryset):
        response = HttpResponse(content_type="application/json")
        serializers.serialize("json", queryset, stream=response)
        return response


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status', 'created_at')
    search_fields = ('customer', 'status')
    list_filter = ('customer', 'status', 'created_at')
    actions = ['make_completed']
    
    @admin.action(description='Make selected orders completed')
    def make_completed(self, request, queryset):
        updated_orders = queryset.update(status='completed')
        #self.message_user(request, 'Selected orders have been completed')
        self.message_user(
            request, 
            ngettext(
                '%d order has been completed', 
                '%d orders have been completed', queryset.count()
                ) % updated_orders,
            messages.SUCCESS
        )   

class InteractionInline(admin.TabularInline):
    model = Interaction
    extra = 1

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('name', 'created_at',)
    inlines = [InteractionInline]
    