from cntapp.models import Directory


def get_root_dirs():
    all_dirs = Directory.objects.all()
    return [d for d in all_dirs if d.get_parents().count() == 0]


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
