from PostgreSQL import Database
from Fang import Pull

if __name__ == "__main__":
    database = Database.DataBase(host="localhost", database="house", user="postgres", password="miaomiaomiao")

    for single in database.pull_all_by_address():
        database.insert_address(single[0], single[1], single[2], single[3], single[4], single[5], single[6])

