import pymongo
import random


client = pymongo.MongoClient("mongodb://localhost:27017")
print('Successfully ', client)

mongodb_name = 'web8'

db = client[mongodb_name]


def insert():
    u = {
        'name': 'wd',
        'random_id': '{}'.format(random.randint(1, 9)),
    }
    db.user.insert(u)


def find_all():
    user_list = list(db.user.find())
    print('All data ', user_list)


def find_args():
    query = {
        'random': 1,
        'name': 'wd',
    }
    print('random 1 user', len(db.user.find(query)))

    # $gt代表大于
    query = {
        'random': {
            '$gt': 1
        },
    }
    print('random $gt 1', db.user.find(query))

    query = {
        '$or': [
            {
                'random': 2,
            },
            {
                'name': 'gua',
            },
        ]
    }
    print('$or ', db.user.find(query))


def find_cond():
    query = {}
    # 1为提取，0则反之
    field = {
        'name': 1,
        '_id': 0,
    }
    print('Data cond ', db.user.find(query, field))


def update():
    query = {
        'random': 1,
    }
    form = {
        '$set': {
            'name': 'update test'
        }
    }
    # 默认只更新查询到的第一条记录， multi为True则更新所有符合条件的记录
    options = {
        'multi': True,
    }
    db.user.update(query, form, **options)


def user_remove():
    query = {
        '_deleted': False,
    }
    user_list = list(db.user.find(query))
    us = []
    for u in user_list:
        u.pop('_deleted')
        us.append(u)
    print('All user ', len(us), us)


if __name__ == '__main__':
    insert()
    find_all()
    find_args()
    find_cond()
    update()
    user_remove()

