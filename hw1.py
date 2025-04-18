from abc import abstractmethod


class DataSource:
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass

class TextFile(DataSource):
    def __init__(self, name):
        self.__content = ""
        self.__name = name

    def read(self):
        return self.__content
    
    def write(self, data):
        self.__content = data

class Database(DataSource):
    def __init__(self, name):
        self.__data = []
        self.__name = name

    def read(self):
        return self.__data
    
    def write(self, data):
        self.__data.append(data)

class NetworkResource(DataSource):
    def __init__(self, url):
        self.__data = ""
        self.__url = url

    def read(self):
        return self.__data
    
    def write(self, data):
        self.__data = data

#DON'T TOUCH UNDER THE LINE
#______________________________________________________________
def process_data(data_source, data=None):
    if data:
        data_source.write(data)
    return data_source.read()

text_file = TextFile("document.txt")
database = Database("users.db")
network = NetworkResource("http://example.com/api")

print(process_data(text_file, "Новый текст"))
print(process_data(database, {"name": "Иван", "age": 25}))
print(process_data(network, "POST data"))