import pika
import json
import threading
import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5673))


class RabbitMQConsumer:
    """Consumidor de mensajes para RabbitMQ"""

    def __init__(self):
        self.connection = None
        self.channel = None
        self.start_consuming()

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

            print(f"✅ Place Service conectado a RabbitMQ en {RABBITMQ_HOST}:{RABBITMQ_PORT}")
        except Exception as e:
            print(f"❌ Place Service error conectando a RabbitMQ: {e}")

    def callback_user_registered(self, ch, method, properties, body):
        """Procesar evento de usuario registrado"""
        try:
            data = json.loads(body)
            print(f"📥 Usuario registrado recibido: {data['username']} (ID: {data['user_id']})")
            print(f"   Evento procesado correctamente")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"❌ Error procesando mensaje: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def callback_user_deleted(self, ch, method, properties, body):
        """Procesar evento de usuario eliminado"""
        try:
            data = json.loads(body)
            print(f"📥 Usuario eliminado recibido: {data['user_id']}")
            print(f"   Evento procesado correctamente")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"❌ Error procesando mensaje: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def start_consuming(self):
        """Iniciar consumo en un hilo separado"""

        def consume():
            try:
                self.connect()
                if self.channel:
                    self.channel.basic_consume(
                        queue='user_registered',
                        on_message_callback=self.callback_user_registered,
                        auto_ack=False
                    )
                    self.channel.basic_consume(
                        queue='user_deleted',
                        on_message_callback=self.callback_user_deleted,
                        auto_ack=False
                    )
                    print("✅ Place Service Consumer iniciado, esperando mensajes...")
                    self.channel.start_consuming()
            except Exception as e:
                print(f"❌ Error en consumidor: {e}")

        thread = threading.Thread(target=consume, daemon=True)
        thread.start()


# Instancia global
rabbitmq_consumer = RabbitMQConsumer()