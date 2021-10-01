'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-09-30 17:50:26
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-01 12:07:33
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
channel.exchange_declare(
    exchange="exchange.test",# 空字符串代表默认或者匿名交换机：消息将会根据指定的routing_key分发到指定的队列。
    exchange_type='fanout', # 直连交换机（direct）, 主题交换机（topic）, （头交换机）headers和 扇型交换机（fanout）,
    durable=True
)

# 创建一个临时队列,不提供queue参数，会自动生成一个随机的队列名
res = channel.queue_declare(
    queue='',
    exclusive= True # 当和消费者断开连接时，该队列被删除
)

print(res,type(res))
# 绑定 producer  exchange  queues
# 要注意这里其实是consumer声明一个队列去绑定
# 模型
#                           binding(receiver绑定)    queue1    ----> consumer1   
#  producer ----> exchange --------------------->   queue2    ----> consumer2
#                                                   queue3    ----> consumer3

channel.queue_bind(
    exchange="exchange.test",
    queue=res.method.queue
)

def callback(channel,method,properties,body):
    print(f"consumer2 get message:{body.decode('utf-8')}")
    channel.basic_ack(delivery_tag = method.delivery_tag)


channel.basic_consume(
    on_message_callback=callback,
    queue=res.method.queue,
    auto_ack=False)

channel.start_consuming()