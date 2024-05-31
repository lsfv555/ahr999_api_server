import json
import globals
import os

# 读取订阅数据
def load_subscriptions():
    try:
        with open('./data/subscriptions.json', 'r') as f:
            subscriptions_data = json.load(f)
            globals.subscriptions = [globals.Subscription(**sub) for sub in subscriptions_data]
    except FileNotFoundError:
        globals.subscriptions = []
    except json.JSONDecodeError:
        globals.subscriptions = []

# 保存订阅数据
def save_subscriptions():
    with open('./data/subscriptions.json', 'w') as f:
        json.dump([sub.to_dict() for sub in globals.subscriptions], f, indent=4)

# 确保数据目录存在
os.makedirs('./data', exist_ok=True)
