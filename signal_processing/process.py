import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import time
from numpy import sin, pi

class Process_signal(Node):
    def __init__(self):
        super().__init__('process')

        # Suscripción a los tópicos 'signal' y 'time'
        self.subscription = self.create_subscription(Float32, 'signal', self.listener_callback, 10)
        self.subscription_time = self.create_subscription(Float32, 'time', self.timer_callback, 10)

        # Publicador para la señal procesada
        self.pub = self.create_publisher(Float32, 'proc_signal', 10)

        self.signal = Float32()  # Mensaje que se publicará
        self.proc_signal = 0  # Almacena la señal recibida
        self.proc_time = 0  # Almacena el tiempo recibido

        # Parámetros de procesamiento de la señal
        self.amplitude = 0.5  # Amplitud de la nueva señal
        self.phase = pi / 2  # Fase de la nueva señal
        self.offset = 0.5  # Desplazamiento en Y

        # Temporizador para el envío periódico de la señal procesada
        self.timer = self.create_timer(0.1, self.sender_callback)

    def listener_callback(self, msg):
        """ Callback que recibe la señal original. """
        self.proc_signal = msg.data

    def timer_callback(self, msg):
        """ Callback que recibe el tiempo de la señal original. """
        self.proc_time = msg.data

    def sender_callback(self):
        """ Callback que genera y publica la señal procesada. """
        self.signal.data = self.amplitude * sin(2 * pi * self.proc_time + self.phase) + self.offset

        self.pub.publish(self.signal)  # Publica la señal procesada

        self.get_logger().info('Signal: "%f"' % self.signal.data)  # Imprime la señal procesada

def main(args=None):
    rclpy.init(args=args)
    process_signal = Process_signal()
    rclpy.spin(process_signal)  # Mantiene el nodo en ejecución
    process_signal.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()