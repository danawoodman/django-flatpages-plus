from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from flatpages_plus.forms import FlatpageForm
from flatpages_plus.models import FlatPage


class FlatPageAdmin(admin.ModelAdmin):
    form = FlatpageForm
    fieldsets = (
        (None, {'fields': (
            'url',
            'title',
            'owner',
            'status',
            'content',
            'tags',
            'sites',
        )}),
        (_('Advanced options'), {
            'classes': ('collapse',), 
            'fields': (
                'enable_comments', 
                'registration_required', 
                'template_name',
                'views',
            )
        }),
    )
    list_display = ('url', 'title', 'status', 'owner',)
    list_filter = ('status', 'sites', 'enable_comments', 'registration_required',)
    search_fields = ('url', 'title', 'owner',)

admin.site.register(FlatPage, FlatPageAdmin)
