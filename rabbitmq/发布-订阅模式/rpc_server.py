'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-01 20:50:45
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-01 22:45:53
'''

# 为每个客户端只建立一个独立的回调队列。
# model
#
#        request. reply_to=queue.tag,correlation_id="test"
#        ------------------------------------------------->  rpc queue   ---------> 
# client                                                                             server   
#       <-----------------------------------------------  replay_to = queue.tag <--------- 
#           replay correlation_id= "test"                                                      

# 当客户端启动的时候，它创建一个匿名独享的回调队列。

# 1 在RPC请求中，客户端发送带有两个属性的消息：一个是设置回调队列的 reply_to 属性，
#   另一个是设置唯一值的 correlation_id 属性。

# 2 将请求发送到一个 rpc_queue 队列中。
# 3 RPC工作者（又名：服务器）等待请求发送到这个队列中来。当请求出现的时候，
#   它执行他的工作并且将带有执行结果的消息发送给reply_to字段指定的队列。
# 4 客户端等待回调队列里的数据。当有消息出现的时候，它会检查correlation_id属性。
#   如果此属性的值与请求匹配，将它返回给应用
# 都是基于队列的

import json
import pika
from pika.credentials import PlainCredentials
import time

def add(*vars):
    res = 0 
    for var in vars:
        res = res +var
    time.sleep(1)
    return res

def sub(var1,var2):
    time.sleep(2)
    return var1 - var2


def print_log(msg):
    return msg

def raise_error():
    try:
        raise RuntimeError("THIS IS TEST RERROR")
    except Exception as e:
        import traceback
        return traceback.format_exc()

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

res = channel.queue_declare(
    queue="rpc_queue_request",
    exclusive=True,
    durable= True
)

def on_request(ch,method,props,body):
    ## 这里是监听rpc_Queue 即每个rpc都有一个所属的 queue 队列,
    ## 当客户端发送请求后，入队，服务端监听到后即为调用 on_request
    print(method,type(method))
    print(props,type(props))  
    print(body,type(body))
    

    request_ = json.loads(body)
    method_name  = request_.get("name")
    args = request_.get("args")
    print(eval(method_name))
    response = eval(method_name)(*args)
    print(f"get rpc request body:{body} ")

    ch.basic_publish(exchange='',
                    routing_key=props.reply_to,
                    properties=pika.BasicProperties(
                        correlation_id = props.correlation_id 
                        # correlation_id用于标记请求，当response queue出现message时，会去检测是否为对应的 request
                        ),
                    body=str(response)) # response必须要序列化
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print(f"rpc method {method_name} called finish! return:{response}")
# 因为服务是不断监听 rpc_queue_request队列，一次只能处理一个，除非用多线程处理服务
channel.basic_qos(prefetch_count=1) # 

print("开始监听rpc客户端请求.........")
channel.basic_consume(on_message_callback= on_request, queue='rpc_queue_request',auto_ack=False)
channel.start_consuming()