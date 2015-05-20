from django.contrib import admin

from cntapp.models import Directory, Document


class DirectoryInline(admin.TabularInline):
    model = Directory.sub_dirs.through
    fk_name = 'parent'
    extra = 1


class DirectoryParentsInline(admin.TabularInline):
    model = Directory.sub_dirs.through
    fk_name = 'child'
    extra = 1


class DirectoryDocumentInline(admin.TabularInline):
    model = Directory.documents.through
    extra = 1


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    inlines = (DirectoryDocumentInline, )


@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Directory Information', {'fields': ['name']}),
    ]
    inlines = (DirectoryInline, DirectoryParentsInline)
