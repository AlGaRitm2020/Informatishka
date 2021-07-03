try:
    from config import DATABASE_URL
except ImportError:
    import DATABASE_URL


def get_db_config_from_url():
    li = DATABASE_URL.split('/')
    DB_NAME = li[-1]
    li_2 = li[2].split(':')
    DB_USER = li_2[0]
    DB_PASS, DB_HOST = li_2[1].split('@')

    db_settings = {
        'dbname': DB_NAME,
        'user': DB_USER,
        'password': DB_PASS,
        'host': DB_HOST
    }
    return db_settings