from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import CustomUser, Organization, Event


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'phone_number')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'address', 'postcode')
    list_filter = ('title', 'postcode')
    search_fields = ('title', 'description')


class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
        'date',
        'display_image_preview'
    )
    list_filter = ('title', 'organizations__title')
    search_fields = ('title', 'description')
    readonly_fields = ('display_image_preview',)

    def display_image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px; max-width: 100px;" />')
        return 'No Image'

    display_image_preview.short_description = 'Image Preview'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Event, EventAdmin)
