from __future__ import absolute_import, unicode_literals

# Configure PyMySQL to work with Django's MySQL backend
# This is needed because Django expects mysqlclient, but pymysql is easier to install
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass  # pymysql not installed, will use mysqlclient if available