import os
import pickle

from dotenv import load_dotenv
from collections import defaultdict


load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
admins = [
    00000
]

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}


with open('C:\\Users\\Тарас\\Programming\\FedMe Bot\\FedMe Bot 2.0\\data\\dataset.pickle', 'rb') as f2:
    dataset_input = pickle.load(f2)

with open('C:\\Users\\Тарас\\Programming\\FedMe Bot\\FedMe Bot 2.0\\data\\BOT_CONFIG.pickle', 'rb') as f4:
    BOT_CONFIG = pickle.load(f4)

with open('C:\\Users\\Тарас\\Programming\\FedMe Bot\\FedMe Bot 2.0\\data\\RECIPES_new.pickle', 'rb') as f5:
    RECIPES = pickle.load(f5)

dataset_search = defaultdict(list)
for ingredient, category in dataset_input:
    words = ingredient.split(' ')
    for word in words:
        dataset_search[word].append([ingredient, category])
