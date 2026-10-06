from django.contrib import admin, messages
from . import models
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse 
from django.contrib.contenttypes.admin import GenericTabularInline
from tags.models import TaggedItem


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'




# Register your models here.
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):#class ProductAdmin Inheriting from modeAdmin
    #inlines = [TagInline]
    list_display = ['tittle','price']
    list_filter = ['tittle','price']
    list_editable = ['price']
    list_per_page = 10 #lists per page
    actions = ['clear_inventory']
    #fields = ['tittle']
    exclude = ['promotion']
    prepopulated_fields = {
        'slug': ['tittle']
    }

class OrderItemInline(admin.TabularInline):
    #autocomplete_fields = ['product']
    model = models.OrderItem
    min_num = 1
    max_num = 10
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','placed_at']
    inlines = [OrderItemInline]
    #autocomplete_fields = ['Customer']



admin.site.register(models.Collection)
#admin.site.register(models.Product, ProductAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','email']
    list_editable = ['email']
    ordering = ['firts_name','last_name']
    list_per_page = 10
    list_filter = ['collection','last_update']
    search_fields = ['first_name__istartswith','last_name__startswith']

@admin.display(ordering='inventory')
def inventory_status(self, product):
    if product.inventory < 10:
        return 'Low'
    return 'OK'

def collection_tittle(self, product):
    return product.collection.tittle

@admin.display(ordering='products_count')
def products_count(self, collection):
    url = (
        reverse('admin:store_product_page') 
        + '?'
        + urlencode({
            'collection_id': str(collection.id)
        }))
    return format_html('<a href={}>{}</a>',url, collection.product_count)
     

def get_querySet(self, request):
    return super().get_querySet(request).annotate(
        products_count=Count('product')
    )

def lookups(self, request, model_admin):
    return[
        ('<10', 'Low')

    ]

def Queryset(self, request, quearyset):
    if self.value() == '<10':
        return quearyset.filter(inventory__lt=10)

@admin.action(description='Clear inventory')
def clear_inventory(self, request, queryset):
    updated_count = queryset.update(inventory=0)
    self.message_user(
        request,
        f'{updated_count} products were successfully updated'

    )

