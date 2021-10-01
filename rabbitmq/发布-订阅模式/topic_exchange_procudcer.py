'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-01 13:55:22
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-01 20:44:20
'''

# 直连交换机的分发会根据绑定键和路由键进行精确匹配


#                                         topic1
#                                       ---------> queue1 -> consumer1
# producer ---> topic exchange ------->
#                                       ---------> queue2 -> consumer2
#                                        topic1/topic2...(多个主题绑定同一个queue)

#                                       ---------> queue3 -> consumer3
                                    #    topic1(同个topic绑定多个queue)


# topic 规范 xxx.yyy.zzz   这些应该是consumer绑定时配置
    #  * (星号) 用来表示一个单词.
    #  # (井号) 用来表示任意数量（零个或多个）单词。
#  *.xxx.*  xxx.#    *.*.rabbit  

# 假设了三个绑定：Q1的绑定键为 *.orange.*，Q2的绑定键为 *.*.rabbit 和 Q3 lazy.# 。
# 这三个绑定键被可以总结为：
#     Q1 对所有的桔黄色动物都感兴趣。
#     Q2 则是对所有的兔子和所有懒惰的动物感兴趣
# quick.orange.rabbit --> Q1 AND Q2
# quick.orange.male.rabbit -> drop
# lazy.orange.male.rabbit  -> Q3


# 当一个队列的绑定键为 "#"（井号） 的时候，这个队列将会无视消息的路由键，接收所有的消息。
# 当 * (星号) 和 # (井号) 这两个特殊字符都未在绑定键中出现的时候，此时主题交换机就拥有的直连交换机的行为


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
# 与 fanout 相比 广播改为 接受特定的消息
channel.exchange_declare(
    exchange="exchange.test.topic",# 空字符串代表默认或者匿名交换机：消息将会根据指定的routing_key分发到指定的队列。
    exchange_type='topic', # 直连交换机（direct）, 主题交换机（topic）, （头交换机）headers和 扇型交换机（fanout）,
    durable=True
)
# 发布一条消息
channel.basic_publish(
    exchange="exchange.test.topic",
    routing_key="test.message",
    body="this is exchange message test",
)

connection.close()