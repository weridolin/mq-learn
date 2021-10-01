'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-01 22:01:38
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-01 22:45:00
'''

import uuid
import pika
import json

class RpaClient(object):
    
    def __init__(self) -> None:

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="localhost",
                port=5672,credentials=pika.credentials.PlainCredentials(
                    username="root",
                    password="root"
                    )
                )
            )
        self.channel = self.connection.channel()

        # 声明一个属于这个客户端的调用链接
        res = self.channel.queue_declare(exclusive=True,queue="")
        self.call_back_queue = res.method.queue
        self.channel.basic_consume(
            on_message_callback= self.on_response,
            auto_ack=True,
            queue=self.call_back_queue)
    
    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = body
        print(f"get response {self.response.decode('utf-8')}")


    def call(self,method,*args):
        request = json.dumps({
            "name":method,
            "args":args
        })
        print(f"rpa request:{request}")

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange="",
            routing_key="rpc_queue_request",
            properties=pika.BasicProperties(
                reply_to=self.call_back_queue,
                correlation_id=self.corr_id
            ),
            body=request
        )

        # 等待远程调用返回值
        while self.response is None:
            self.connection.process_data_events()
        return self.response

rpc_client = RpaClient()
rpc_client.call("add",1,3,4,5,6)
rpc_client.call("sub",6,1)
rpc_client.call("print_log","test")
rpc_client.call("raise_error")