'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-01 13:55:22
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-01 18:33:36
'''

# 直连交换机的分发会根据绑定键和路由键进行精确匹配

#                                         key1
#                                       -------> queue1 -> consumer1
# producer ---> direct exchange ------->
#                                       -------> queue2 -> consumer2
#                                        key2/key3...(多个路由绑定同一个queue)

#                                       -------> queue3 -> consumer3
                                    #    key1(同个key绑定多个queue)



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
# 通过exchange的值和routing_key的值来确定要收到的消息，
# 与 fanout 相比 广播改为 接受特定的消息 fanout会忽略 routing_key 值
channel.exchange_declare(
    exchange="exchange.test.direct",# 空字符串代表默认或者匿名交换机：消息将会根据指定的routing_key分发到指定的队列。
    exchange_type='direct', # 直连交换机（direct）, 主题交换机（topic）, （头交换机）headers和 扇型交换机（fanout）,
    durable=True
)
# 发布一条消息
channel.basic_publish(
    exchange="exchange.test.direct",
    routing_key="directExchangeRouteKey1",
    body="this is exchange message test",
)
