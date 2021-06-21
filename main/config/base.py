class _Config(object):
    MYSQL_HOST = None
    MYSQL_PORT = None
    MYSQL_USERNAME = None
    MYSQL_PASSWORD = None
    MYSQL_DB = None
    DEBUG = False
    ITEM_PER_PAGE = None

    @classmethod
    def get_sqlalchemy_db_uri(cls):
        return f"mysql+pymysql://{cls.MYSQL_USERNAME}:{cls.MYSQL_PASSWORD}@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DB}"
