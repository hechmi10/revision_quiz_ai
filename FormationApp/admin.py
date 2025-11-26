from django.contrib import admin
from FormationApp.models import Formation
# Register your models here.
@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ("titre", "description", "niveau")
    search_fields = ("titre", "description")
    list_filter = ("niveau",)
    ordering = ("titre",)
    fieldsets = (
        (None, {
            "fields": ("titre", "description", "niveau", "domaine", "creator")
        }),
    )
admin.site.site_header = "Revision Quiz AI Admin"
admin.site.site_title = "Revision Quiz AI Admin Portal"
admin.site.index_title = "Welcome to Revision Quiz AI Admin Portal"