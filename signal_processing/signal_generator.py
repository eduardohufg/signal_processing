import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from numpy import sin, pi, cos
import time
from scipy import signal

class SignalCode(Node):
    def __init__(self):
        super().__init__('signal_generator')
        
        # Creación de los publicadores para la señal y el tiempo
        self.pub_signal = self.create_publisher(Float32, 'signal', 10)
        self.pub_time = self.create_publisher(Float32, 'time', 10)
        
        self.msg = Float32()
        self.msg_time = Float32()

        # Definición de parámetros iniciales del generador de señales

        self.declare_parameter('amplitude', 1.0)  # Amplitud de la señal
        self.declare_parameter('phase', 0.0)  # Fase inicial
        self.declare_parameter('offset', 0.0)  # Desplazamiento en Y
        self.declare_parameter('period', 2)  # Periodo de la señal
        self.declare_parameter('sample_time', 0.1)  # Tiempo de muestreo
        self.declare_parameter('type', 1)  # Tipo de señal

        # Obtención de los valores de los parámetros
        self.amplitude = self.get_parameter('amplitude').value
        self.frequency = 1 / self.get_parameter('period').value
        self.phase = self.get_parameter('phase').value
        self.offset = self.get_parameter('offset').value
        self.sample_time = self.get_parameter('sample_time').value
        self.type = self.get_parameter('type').value

        self.t0 = time.time()  # Tiempo de inicio
        
        # Creación de temporizadores
        self.timer = self.create_timer(self.sample_time, self.timer_callback)  # Genera la señal periódicamente
        self.timer2 = self.create_timer(3, self.param_callback)  # Actualiza los parámetros cada 3 segundos

    def param_callback(self):
        """ Callback para actualizar los parámetros en tiempo de ejecución. """
        self.amplitude = self.get_parameter('amplitude').value
        self.frequency = 1 / self.get_parameter('period').value
        self.phase = self.get_parameter('phase').value
        self.offset = self.get_parameter('offset').value
        self.sample_time = self.get_parameter('sample_time').value
        self.type = self.get_parameter('type').value

    def timer_callback(self):
        """ Callback principal que genera la señal y la publica. """
        t = time.time() - self.t0  # Tiempo transcurrido desde el inicio
        
        # Generación de la señal según el tipo especificado
        if self.type == 1:
            self.msg.data = self.amplitude * sin(2 * pi * self.frequency * t + self.phase) + self.offset
        elif self.type == 2:
            self.msg.data = self.amplitude * cos(2 * pi * self.frequency * t + self.phase) + self.offset
        elif self.type == 3:
            self.msg.data = signal.sawtooth(2 * pi * self.frequency * t + self.phase, .5) + self.offset  # Triangular
        elif self.type == 4:
            self.msg.data = signal.square(2 * pi * self.frequency * t + self.phase) + self.offset  # Cuadrada
        elif self.type == 5:
            self.msg.data = signal.sawtooth(2 * pi * self.frequency * t + self.phase, 1) + self.offset  # Diente de sierra ascendente
        elif self.type == 6:
            self.msg.data = signal.sawtooth(2 * pi * self.frequency * t + self.phase, 0) + self.offset  # Diente de sierra descendente

        # Publicación de la señal y el tiempo
        self.msg_time.data = t
        self.pub_time.publish(self.msg_time)
        self.pub_signal.publish(self.msg)

        # Registro de la señal generada
        self.get_logger().info('Signal: "%f"' % self.msg.data)
        self.get_logger().info('Time: "%f"' % self.msg_time.data)

def main(args=None):
    """ Función principal que inicia el nodo ROS2. """
    rclpy.init(args=args)
    signal_code = SignalCode()
    rclpy.spin(signal_code)  # Mantiene el nodo en ejecución
    signal_code.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
