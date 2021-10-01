'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-09-30 11:04:55
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-09-30 17:21:15
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
channel.queue_declare(queue="hello-rabbitmq") 


for i in range(9):
    #  rabbitmq会按照consumers队列的顺序下发
    #  假设 msg 对应的标记为 m1--m10
    #  consumers list的顺序为 c1-c3
    #  则有： c1->[m1 m4 m7 m10]  c2->[m2 m5 m8] c3->[m3 m6 m9]    
    channel.basic_publish(
        exchange="",
        routing_key="hello-rabbitmq",
        body=f"this is 第{i}个 message",
    )
