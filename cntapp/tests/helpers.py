from cntapp.models import Directory


def create_dir(name):
    d = Directory(name=name)
    d.save()
    return d


def init_test_dirs():
    """
    create the dir graph:
   a     b     c
    \   |      |
    ab_a      /
   /   \    /
ab_a_a  ab_a_b
    """
    a = create_dir('a')
    b = create_dir('b')
    c = create_dir('c')
    ab_a = create_dir('ab_a')
    ab_a_a = create_dir('ab_a_a')
    ab_a_b = create_dir('ab_a_b')

    a.add_sub_dir(ab_a)
    b.add_sub_dir(ab_a)
    ab_a.add_sub_dir(ab_a_a).add_sub_dir(ab_a_b)
    c.add_sub_dir(ab_a_b)
