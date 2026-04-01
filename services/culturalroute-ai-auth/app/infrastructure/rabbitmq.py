import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5673))


class RabbitMQProducer:
    """Productor de mensajes para RabbitMQ"""

    def __init__(self):
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    port=RABBITMQ_PORT
                )
            )
            self.channel = self.connection.channel()

            # Declarar colas
            self.channel.queue_declare(queue='user_registered', durable=True)
            self.channel.queue_declare(queue='user_deleted', durable=True)

            print(f"✅ Auth Service conectado a RabbitMQ en {RABBITMQ_HOST}:{RABBITMQ_PORT}")
        except Exception as e:
            print(f"❌ Auth Service error conectando a RabbitMQ: {e}")

    def publish(self, queue: str, message: dict):
        """Publicar mensaje en una cola"""
        if not self.channel:
            self.connect()

        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=queue,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                )
            )
            print(f"📤 Mensaje enviado a {queue}: {message}")
        except Exception as e:
            print(f"❌ Error enviando mensaje: {e}")

    def close(self):
        if self.connection:
            self.connection.close()


# Instancia global para usar en toda la aplicación
rabbitmq = RabbitMQProducer()