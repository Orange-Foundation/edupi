from django.contrib.admin.sites import AdminSite


class CMS(AdminSite):
    def __init__(self):
        super().__init__()


cms_site = CMS()
