'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-09-30 17:50:26
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-01 13:53:37
'''
import sys
import pika
from pika.credentials import PlainCredentials

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost",
        port=5672,credentials=PlainCredentials(
            username="root",
            password="root"
            )
        )
    )
channel = connection.channel()
# 广播，适合群发消息通知，客户端必须同时在线才能收到
channel.exchange_declare(
    exchange="exchange.test",# 空字符串代表默认或者匿名交换机：消息将会根据指定的routing_key分发到指定的队列。
    exchange_type='fanout', # 直连交换机（direct）, 主题交换机（topic）, （头交换机）headers和 扇型交换机（fanout）,
    durable=True
)
# 发布一条消息
channel.basic_publish(
    exchange="exchange.test",
    routing_key="",#  fanout会忽略 routing_key 值
    body="this is exchange message test"
)

# 模型
#                           binding(receiver绑定)    queue1    ----> consumer1   
#  producer ----> exchange --------------------->   queue2    ----> consumer2
#                                                   queue3    ----> consumer3
