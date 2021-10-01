'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-09-30 08:03:47
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-09-30 17:51:04
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

# 创建一个队列,可以多次调用，但是最终只会有一个
r = channel.queue_declare(queue="hello-rabbitmq")
print(r)


def get_msg_callback(ch, method, properties, body):
    # 第一个为channel 实例

    print("receiver_with_no_auto_ack get body",type(body),body.decode("utf-8"))
    # 
    # ch.basic_ack(delivery_tag = method.delivery_tag)
    
channel.basic_qos(prefetch_count=1) 
# 再同一时刻，不要发送超过1条消息给一个工作者（worker），直到它已经处理了上一条消息并且作出了响应

channel.basic_consume(
    on_message_callback= get_msg_callback,
    queue="hello-rabbitmq",
    auto_ack=False
)

# 开始一个轮询不断消费
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()