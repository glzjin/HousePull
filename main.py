from TextInsert import Database
from Fang import Pull

if __name__ == "__main__":
    database = Database.DataBase(host="localhost", database="house", user="postgres", password="miaomiaomiao")

    # database.insert("test2", "test234", 1.22, 1.33, 1.44, 1.55)

    fang_pull = Pull.Pull()
    fang_pull.pull_and_insert(database)