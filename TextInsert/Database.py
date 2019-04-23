import threading


class DataBase:
    def __init__(self, host="localhost", database="twitter", user="postgres", password="123456"):
        self.fo = open(database + '.sql', 'w')
        self.mutex = threading.Lock()

    def __del__(self):
        self.fo.close()

    def insert(self, name, address, longitude, latitude, price, area):
        self.mutex.acquire()
        if longitude == '':
            longitude = 0.0

        if latitude == '':
            latitude = 0.0
        self.fo.writelines("INSERT INTO house_origin VALUES (DEFAULT, '%s', '%s', %s, %s, %s, %s);" %
                        (name, address, longitude, latitude, price, area) + ";\n")
        # print("INSERT INTO house_origin VALUES (DEFAULT, '%s', '%s', %s, %s, %s, %s);" %
        #                 (name, address, longitude, latitude, price, area))
        self.fo.flush()
        self.mutex.release()

    def pull_all(self):
        pass

    def pull_all_by_address(self):
        pass