import pika


class MessageBroker:
    def __init__(self):
        self.connection = None
        self.channel = None
    
    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

    def publish_to_queue(self, transactions, queue_name):
        self.channel.queue_declare(queue=queue_name)

        for transaction in transactions:
            self.channel.basic_publish(exchange='', routing_key=queue_name, body=str(transaction))
        