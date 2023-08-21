from mongoengine import connect

def connection_to_mongo():
    connect(db='pyweb_module_09', host='localhost', port=27017)