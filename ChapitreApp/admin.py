from django.contrib import admin

from ChapitreApp.models import Chapitre

# Register your models here.
@admin.register(Chapitre)
class ChapitreAdmin(admin.ModelAdmin):
    list_display = ("titre", "get_formation_titre", "ordre")
    search_fields = ("titre", "formation__titre")
    list_filter = ("formation",)
    ordering = ("formation__titre", "ordre")
    fieldsets = (
        (None, {
            "fields": ("titre", "contenu_texte", "ordre")
        }),
        ("Formation", {
            "fields": ("formation",)
        }),
    )
    actions = ['make_ordered']
    
    def get_formation_titre(self, obj):
        return obj.formation.titre
    get_formation_titre.short_description = 'Formation'
    get_formation_titre.admin_order_field = 'formation__titre'
admin.site.site_header = "Revision Quiz AI Admin"
admin.site.site_title = "Revision Quiz AI Admin Portal"
admin.site.index_title = "Welcome to Revision Quiz AI Admin Portal"