from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from environs import Env

env = Env()
env.read_env()

client = MongoClient(f"mongodb+srv://{env('DB_USERNAME')}:{env('DB_PASSWORD')}@cluster0.kdtlt.mongodb.net/")

db = client.book


def get_all_cats():
    try:
        cats = db.cats.find()
        for cat in cats:
            print(cat)
    except ConnectionFailure as e:
        print(f"Помилка при підключенні до MongoDB: {e}")


def get_cat_by_name(name:str):
    try:
        cat = db.cats.find_one({"name": name})
        if cat is None:
            print('Такого кота в базі даних немає')
        else:
            print(cat)
    except ConnectionFailure as e:
        print(f"Помилка при підключенні до MongoDB: {e}")


def update_cat_age(name:str, new_age):
    try:
        if db.cats.count_documents({"name": name}) == 0:
            print(f"Немає такого кота {name}")
        else:
            result = db.cats.update_one({"name": name}, {"$set": {"age": new_age}})
            if result.modified_count > 0:
                print(f"Тепер коту {name} {new_age} років")
            else:
                print(f"Нічого не змінено, бо коту {name} вже {new_age} років")
    except ConnectionFailure as e:
        print(f"Помилка при підключенні до MongoDB: {e}")


def update_cat_features(name:str, feature:str):
    try:
        if db.cats.count_documents({"name": name}) == 0:
            print(f"Немає такого кота {name}")
        else:
            cat = db.cats.find_one({"name": name, "features": feature})
            if cat:
                print(f"Кіт {name} вже має характеристику {feature}")
            else:
                result = db.cats.update_one({"name": name}, {"$push": {"features": feature}})
                if result.modified_count > 0:
                    print(f"Тепер кіт {name} має нову характеристику {feature}")
                else:
                    print(f"Нічого не змінено, бо виникла невідома помилка.")
    except ConnectionFailure as e:
        print(f"Помилка при підключенні до MongoDB: {e}")


def delete_cat(name):
    try:
        if db.cats.count_documents({"name": name}) == 0:
            print(f"Немає такого кота {name}")
        else:
            db.cats.delete_one({"name": name})
            print(f"Видалено кота {name}")
    except ConnectionFailure as e:
        print(f"Помилка при підключенні до MongoDB: {e}")


def delete_cats():
    try:
        if db.cats.count_documents({}) == 0:
            print("База даних попрожня")
        else:
            db.cats.delete_many({})
            print("Видалено всіх котів")
    except ConnectionFailure as e:
        print(f"Помилка при підключенні до MongoDB: {e}")


if __name__ == "__main__":
    get_all_cats()
    get_cat_by_name('barsi')
    update_cat_age('Lama', 6)
    update_cat_features('barsik', 'курить')
    delete_cat('Lama')
    delete_cats()