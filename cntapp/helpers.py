from cntapp.models import Directory, SubDirRelation


def queryset_to_list(query_set):
    return [d for d in query_set]


def get_root_dirs_query():
    """
    Directories that has no parent are root directories.

    steps:
    1. select all parents' id from SubDirRelation.
    2. exclude directories that have parents
    """
    r = SubDirRelation.objects.values('parent').distinct()
    l = [d['parent'] for d in r]

    # FIXME:
    # attention: child is a SubDirRelation object that relates to the directory's parent !
    # then the parent_id point to it's real parent Directory object.
    # This was a confuse when building the API.
    return Directory.objects.exclude(child__parent_id__in=l)


def get_root_dirs():
    return queryset_to_list(get_root_dirs_query())


def get_root_dirs_names():
    all_dirs = Directory.objects.all()
    return [d.name for d in all_dirs if d.get_parents().count() == 0]


def get_dir_by_path(url):
    if len(url) == 0:
        return None

    dir_names = url.split('/')
    root_dir = [d for d in (get_root_dirs()) if d.name == dir_names[0]][0]

    current_dir = root_dir

    for dir_name in dir_names[1:]:
        sub_dir_names = [d.name for d in current_dir.get_sub_dirs()]
        if dir_name not in sub_dir_names:
            return None
        else:
            current_dir = current_dir.get_sub_dirs().get(name=dir_name)

    return current_dir
