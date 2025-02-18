#generate a sinusoide signal and i can change the amplitude, frequency, phase and offset

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from numpy import sin, pi, cos
import time
import sys
from scipy import signal

class SignalCode(Node):
    def __init__(self):
        super().__init__('signal_generic')
        self.pub_signal = self.create_publisher(Float32, 'signal_generic', 10)
        self.pub_time = self.create_publisher(Float32, 'time_generic', 10)
        self.msg = Float32()
        self.msg_time = Float32()
        self.amplitude = float(sys.argv[1])
        self.frequency = 1/float(sys.argv[4])
        self.phase = float(sys.argv[2])
        self.offset = float(sys.argv[3])
        self.sample_time = float(sys.argv[5])
        self.type = int(sys.argv[6])
        self.timer = self.create_timer(self.sample_time, self.timer_callback)
        self.t0 = time.time()

    def timer_callback(self):

        t = time.time() - self.t0
        
        if self.type == 1:

            self.msg.data = self.amplitude * sin(2 * pi * self.frequency * t + self.phase) + self.offset
        elif self.type == 2:
            self.msg.data = self.amplitude * cos(2 * pi * self.frequency * t + self.phase) + self.offset
        
        #triangular signal
        elif self.type == 3:
            self.msg.data = signal.sawtooth(2 * pi * self.frequency * t + self.phase, .5) + self.offset
        #square signal
        elif self.type == 4:
            self.msg.data = signal.square(2 * pi * self.frequency * t + self.phase) + self.offset
        #diente de sierra creciente
        elif self.type == 5:
            self.msg.data = signal.sawtooth(2 * pi * self.frequency * t + self.phase, 1) + self.offset
        #diente de sierra decreciente
        elif self.type == 6:
            self.msg.data = signal.sawtooth(2 * pi * self.frequency * t + self.phase, 0) + self.offset


        
        self.msg_time.data = t
        
        self.pub_time.publish(self.msg_time)
        self.pub_signal.publish(self.msg)

        
        #logger signal and time
        
        self.get_logger().info('Signal: "%f"' % self.msg.data)
        self.get_logger().info('Time: "%f"' % self.msg_time.data)

def main(args=None):
    if len(sys.argv) < 1:
        print("Usage: amplitude phase offset period sample_time type_of_signal")
        sys.exit(1)
        return
    rclpy.init(args=args)
    signal_code = SignalCode()
    rclpy.spin(signal_code)
    signal_code.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()



   