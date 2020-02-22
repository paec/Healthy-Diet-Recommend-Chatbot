import pymongo
import json

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["mydatabase"]

df = db['DisFood']

# d = "急性肝炎"
# result = df.find_one({"Dis":d})
# print(result['Food'])

def getfood(d):

    result = df.find_one({"Dis":d})
    result = result['Food'] if result else []
    jsonresult = json.dumps(result,ensure_ascii=False)

    return jsonresult


# with open("food_suggestion.json","r",encoding="utf8") as r:

#     data = json.loads(r.read())

#     for d in data:

#         df.insert({"Dis":d,"Food":data[d]})


# print(client.list_database_names())
# a = df.index_information()
# print(a)
# df.create_index('Dis')



# df.drop_index('Dis_1')
# a = df.index_information()
# print(a)


# with open("food_suggestion.json","r",encoding="utf8") as r:

#     data = json.loads(r.read())

#     for i in range(20):
#         for d in data:
#             result = df.find_one({"Dis":d})
#             print(result['Dis'])

