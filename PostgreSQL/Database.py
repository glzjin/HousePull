import psycopg2 as psycopg2


class DataBase:
    def __init__(self, host="localhost", database="twitter", user="postgres", password="123456"):
        self.conn = psycopg2.connect(host=host, database=database, user=user, password=password)

    def insert(self, name, address, longitude, latitude, price, area):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO house_origin VALUES (DEFAULT, %s, %s, %s, %s, %s, %s);",
                    (name, address, longitude, latitude, price, area))
        self.conn.commit()
        cur.close()

    def pull_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM house_origin where longitude = 0.0;")
        data = cur.fetchall()
        cur.close()
        return data

    def update_location(self, id, longitude, latitude):
        cur = self.conn.cursor()
        cur.execute("UPDATE house_origin SET longitude = %s, latitude = %s where id = %s;",
                    (longitude, latitude, id))
        self.conn.commit()
        cur.close()

    def pull_all_by_address(self):
        cur = self.conn.cursor()
        cur.execute("select house_address, longitude, latitude, sum(price) as price_sum, sum(area) as area_sum, sum(price) / sum(area) as avg_price,count(*) as count from house_origin group by house_address, longitude, latitude;")
        data = cur.fetchall()
        cur.close()
        return data

    def insert_address(self, address, longitude, latitude, price_sum, area_sum, avg_price, count):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO addresses(id, address, longitude, latitude, total_price, total_area, avg_price, house_count) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s);",
                    (address, longitude, latitude, price_sum, area_sum, avg_price, count))
        self.conn.commit()
        cur.close()