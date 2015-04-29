from django.contrib import admin
from django.contrib.admin.utils import quote
from django.contrib.admin.views.main import ChangeList

from cntapp.models import Directory, Document


class DirectoryInline(admin.TabularInline):
    model = Directory.sub_dirs.through
    fk_name = 'parent'
    extra = 1


class DirectoryParentsInline(admin.TabularInline):
    model = Directory.sub_dirs.through
    fk_name = 'child'
    extra = 1


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


class LevelFilter(admin.SimpleListFilter):
    title = 'level'
    parameter_name = 'pk'

    def __init__(self, request, params, model, model_admin):
        super().__init__(
            request, params, model, model_admin)
        params.clear()  # FIXME url length grows with this!

    def has_output(self):
        return super().has_output()

    def lookups(self, request, model_admin):
        res = list()
        for d in Directory.objects.all():
            res.append((str(d.id), d.name))
        return res

    def queryset(self, request, queryset):
        if self.value() is not None:
            res = queryset.get(id=int(self.value()))
            return res.get_sub_dirs()
        else:
            return queryset.filter(name='root')


class DirChangeList(ChangeList):
    def url_for_result(self, result):
        # pk = getattr(result, self.pk_attname)
        # return reverse('admin:%s_%s_changelist' % (self.opts.app_label, self.opts.model_name),
        #                # args=(quote(pk),),
        #                current_app=self.model_admin.admin_site.name) + ("?pk=%d" % pk)
        return '?pk=%d' % quote(getattr(result, self.pk_attname))

    def get_query_string(self, new_params=None, remove=None):
        return super().get_query_string(new_params, remove)


@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Directory Information', {'fields': ['name']}),
    ]
    inlines = (DirectoryInline, DirectoryParentsInline)
    list_filter = [LevelFilter]

    def add_view(self, request, form_url='', extra_context=None):
        return super().add_view(request, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def get_changelist(self, request, **kwargs):
        return DirChangeList

    def get_urls(self):
        from django.conf.urls import patterns

        info = 'cntapp', 'directory'
        urlpatterns = patterns('',
                               )
        return urlpatterns + super().get_urls()

    def change_view(self, request, object_id, form_url='', extra_context=None):
        return super().changelist_view(request, extra_context)
