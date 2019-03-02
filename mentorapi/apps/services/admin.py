from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import Category, Service, ServicePicture, Review, Favorite


class CategoryAdmin(MPTTModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['token', 'name', 'slug', 'price', 'get_category', 'purchases',
                    'is_available', 'created_at', 'updated_at']
    list_filter = ['is_available', 'created_at', 'updated_at']
    list_editable = ['price', 'name', 'is_available']
    prepopulated_fields = {'slug': ('name',)}

    def get_category(self, obj):
        return "\n".join([c.name for c in obj.category.all()])


admin.site.register(Service, ServiceAdmin)
admin.site.register(ServicePicture)
admin.site.register(Review)
admin.site.register(Favorite)
