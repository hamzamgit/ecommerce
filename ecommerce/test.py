from ecommerce.settings import *

for db_name in ['default']:
    DATABASES[db_name]['ENGINE'] = 'django.db.backends.sqlite3'
    DATABASES[db_name]['NAME'] = ':memory:'
    DATABASES[db_name]['OPTIONS'] = {}
