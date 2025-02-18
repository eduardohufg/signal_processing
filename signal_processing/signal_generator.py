#generate a sinusoide signal and i can change the amplitude, frequency, phase and offset

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from numpy import sin, pi
import time

class SignalCode(Node):
    def __init__(self):
        super().__init__('signal_generator')
        self.pub_signal = self.create_publisher(Float32, 'signal', 10)
        self.pub_time = self.create_publisher(Float32, 'time', 10)
        self.msg = Float32()
        self.msg_time = Float32()
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.amplitude = 1
        self.frequency = 0.5
        self.phase = 0
        self.offset = 0
        self.t0 = time.time()

    def timer_callback(self):

        t = time.time() - self.t0
        

        self.msg.data = self.amplitude * sin(2 * pi * self.frequency * t + self.phase) + self.offset
        self.msg_time.data = t
        
        self.pub_time.publish(self.msg_time)
        self.pub_signal.publish(self.msg)

        
        #logger signal and time
        
        self.get_logger().info('Signal: "%f"' % self.msg.data)
        self.get_logger().info('Time: "%f"' % self.msg_time.data)

def main(args=None):
    rclpy.init(args=args)
    signal_code = SignalCode()
    rclpy.spin(signal_code)
    signal_code.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()



   