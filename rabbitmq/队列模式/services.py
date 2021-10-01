'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-09-29 22:07:25
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-09-30 07:58:10
'''


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

# 创建一个队列
r = channel.queue_declare(queue="hello-rabbitmq")
print(r)

# 发送第一条消息
channel.basic_publish(
    exchange="",
    routing_key="hello-rabbitmq",
    body="this is first message!"
)

connection.close() # 确认网络缓冲已经被刷写、消息已经投递到RabbitMQ