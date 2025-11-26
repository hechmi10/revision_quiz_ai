from django.contrib import admin

from ChapitreApp.models import Chapitre

# Register your models here.
@admin.register(Chapitre)
class ChapitreAdmin(admin.ModelAdmin):
    list_display = ("titre", "formation__titre", "ordre")
    search_fields = ("titre", "formation__titre")
    list_filter = ("formation__titre",)
    ordering = ("formation__titre", "ordre")
    fieldsets = (
        (None, {
            "fields": ("titre", "contenu_texte", "ordre")
        }),
        ("Formation", {
            "fields": ("formation__titre",)
        }),
    )
    actions = ['make_ordered']
admin.site.site_header = "Revision Quiz AI Admin"
admin.site.site_title = "Revision Quiz AI Admin Portal"
admin.site.index_title = "Welcome to Revision Quiz AI Admin Portal"