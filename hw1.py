class TextFile:
    pass

class Database:
    pass

class NetworkResource:
    pass

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