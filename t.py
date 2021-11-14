import os
import urllib.parse as up
import psycopg2

up.uses_netloc.append("postgres")
url = up.urlparse(os.environ["postgres://hzudggdn:wDvu8befix1OG75oDQ4UV-BIZjhlQzfn@fanny.db.elephantsql.com/hzudggdn"])
conn = psycopg2.connect(database=url.path[1:],
user=url.username,
password=url.password,
host=url.hostname,
port=url.port
)