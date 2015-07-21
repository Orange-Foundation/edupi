from enum import Enum


class Header(Enum):
    """
    OrderedDict([
        ('\ufeffid_datas', 0),
        ('titre', 1),
        ('auteur', 2),
        ('pays', 3),
        ('url_doc', 4),
        ('langue', 5),
        ('CYCLE', 6),
        ('CLASSE', 7),
        ('ID CYCLE', 8),
        ('ID_CLASSE', 9),
        ('descriptif', 10),
        ('url_logo', 11),
        ('ok', 12),
        ('date_maj', 13),
        ('MATIERE', 14),
        ('NIVEAU_1', 15),
        ('NIVEAU_2', 16),
        ('ordre', 17),
        ('nv', 18),
        ('', 19),
        ('Absent : 123', 20),
        ('MN1N2', 21),
        ('1893', 22),
        ('TUNFRFR', 23),
        ('\n', 24)
    ])
    """
    name = 1
    filename = 4
    id_cycle = 8
    id_class = 9
    description = 10
    ok = 12

    cycle = 6
    klass = 7
    matiere = 14
    level_1 = 15
    level_2 = 16
