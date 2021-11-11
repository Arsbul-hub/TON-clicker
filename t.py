import psycopg2

conn = psycopg2.connect(database="rasp_pi_db", user="arseni", password="arseni", host="192.168.0.106", port=5432)
cur = conn.cursor()
cur.execute(f"INSERT INTO test_mp.test_obj (timer, x, y, z) VALUES ('{t}', {x}, {y}, {z})")