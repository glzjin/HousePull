from AMap import Utils
from PostgreSQL import Database

if __name__ == "__main__":
    database = Database.DataBase(host="localhost", database="house", user="postgres", password="miaomiaomiao")

    for data in database.pull_all():
        result = Utils.transform("北京" + data[2])
        print(result)

        database.update_location(data[0], result[0], result[1])
