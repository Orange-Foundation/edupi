from django.contrib import admin
from cntapp.models import Directory, Document


class DocumentInline(admin.TabularInline):
    model = Directory.documents.through


class DirectoryInline(admin.TabularInline):
    model = Directory.sub_dirs.through
    fk_name = 'parent'
    extra = 1


class DirectoryParentsInline(admin.TabularInline):
    model = Directory.sub_dirs.through
    fk_name = 'child'
    extra = 1


class DirectoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Directory Information', {'fields': ['name']}),
    ]
    inlines = (DirectoryInline, DirectoryParentsInline)


admin.site.register(Document)
admin.site.register(Directory, DirectoryAdmin)
