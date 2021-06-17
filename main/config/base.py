class _Config(object):
    MYSQL_HOST = None
    MYSQL_PORT = None
    MYSQL_USERNAME = None
    MYSQL_PASSWORD = None
    MYSQL_DB = None
    DEBUG = False

    @classmethod
    def get_sqlalchemy_db_uri(self):
        return f"mysql+pymysql://{self.MYSQL_USERNAME}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
