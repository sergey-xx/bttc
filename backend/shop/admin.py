from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Category, Item, SubCategory, ShoppingCart, CartItem

User = get_user_model()


@admin.register(User)
class UsertAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    pass


class ItemsInlineAdmin(admin.TabularInline):
    """Класс для вывода Товаров в корзине."""

    model = ShoppingCart.items.through
    min_num = 1


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    
    inlines = (ItemsInlineAdmin,)