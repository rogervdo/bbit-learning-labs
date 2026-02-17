
import pika
import os
from producer_interface import mqProducerInterface

class mqProducer(mqProducerInterface):
    def __init__(self, routing_key: str, exchange_name: str):
        #save variables
        self.routing_key = routing_key
        self.exchange = exchange_name

        # Call setupRMQConnection
        self.setupRMQConnection()
        

    def setupRMQConnection(self):
        conParams = pika.URLParameters(os.environ['AMQP_URL'])

        # Establish Channel
        #conectar
        self.connection = pika.BlockingConnection(parameters=conParams)
        self.channel = self.connection.channel()

        #Create the exchange if not already present
        self.channel.exchange_declare(self.exchange)
        

    def publishOrder(self, message: str) -> None:
        # Basic Publish to Exchange
        #We can then publish data to that exchange using the basic_publish method
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.routing_key,
            body=message,
        )
        
        # #define queue
        # self.channel.queue_declare(queue="Tech Lab Queue")
        # #bind queue to exchange
        # self.channel.queue_bind(
        #     queue="Tech Lab Queue",
        #     exchange=self.exchange,
        # )

        # Close Channel
        self.channel.close()

        # Close Connection
        self.connection.close()
        
        
        