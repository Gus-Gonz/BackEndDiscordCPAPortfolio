from pymongo import MongoClient
from config.config_mongo import mongo_client_details ,mongo_cluster , mongo_colection

# --------------------------------REALIZAR CONECCION-------------------------------#
Cluster = MongoClient(mongo_client_details)
db = Cluster[mongo_cluster]
collection = db[mongo_colection]

# --------------------------------AGREGAR A LA DB-------------------------------#

def Add_DB(Combo, Tipo):
    for i in range(len(Combo)):
        USER = Combo[i].split(':')[0]
        PASS = Combo[i].split(':')[1]
        collection.insert_one({'USER': USER, 'PASS': PASS, 'TYPE': Tipo, 'TOKEN': ' '})
    # print('We added {} rows to the DB "Discord-web" under the CLASS = {} '.format(len(Combo),Tipo))
    return True


# --------------------------------EXTRAER ELEMENTO-------------------------------#

def Ext_DB_token(Token):  # ---------------------CHECK IF THE TOKEN HAS BEEN USED---------------------#
    results = collection.find({'TOKEN': Token})
    for ele in results:
        # print ('User:', ele['USER'] ,'\nPass:', ele['PASS'], '\nTipo:',ele['TYPE'])
        return [ele['USER'], ele['PASS'], ele['TYPE']]


def Ext_DB(Tipo, Token):  # ---------------------ADD THE TOKEN TO THE DB---------------------#
    results = collection.find({'TOKEN': ' ', 'TYPE': Tipo})
    for ele in results:
        # print ('User:', ele['USER'],'\nPass:', ele['PASS'])
        Search_id = ele['_id']
        collection.update_one({'_id': Search_id}, {'$set': {'TOKEN': Token}})
        return [ele['USER'], ele['PASS']]


def Check_DB(Tipo):  # ---------------------CHECK THE STOCK---------------------#
    results = collection.count_documents({'TYPE': Tipo, 'TOKEN': ' '})
    return results


def EraseFrom_DB(Tipo, Num):
    results = collection.find({'TOKEN': ' ', 'TYPE': Tipo})
    print(Tipo)
    print(Num)
    for ele in results[:int(Num)]:
        Search_id = ele['_id']
        collection.delete_one({'_id': Search_id})
