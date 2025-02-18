
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import time

class Process_signal(Node):
    def __init__(self):
        super().__init__('process')
        self.subscription = self.create_subscription(Float32, 'signal', self.listener_callback, 10)
        self.subscription_time = self.create_subscription(Float32, 'time', self.timer_callback, 10)
        self.pub = self.create_publisher(Float32, 'proc_signal', 10)
        self. signal = Float32()
        self.subscription
        self.proc_signal = 0    
        self.proc_time = 0
        self.amplitude = 0.5
        self.phase = 0
        self.offset = 0.5
        self.timer = self.create_timer(0.1, self.sender_callback)


    def listener_callback(self, msg):
        self.proc_signal = msg.data

    def timer_callback(self, msg):
        self.proc_time = msg.data
 
    def sender_callback(self):

        #add ofsset, amplitude and phase to the signal received

        self.signal.data = self.amplitude * self.proc_signal + self.offset

        

        self.pub.publish(self.signal)

        self.get_logger().info('Signal: "%f"' % self.signal.data)

def main(args=None):
    rclpy.init(args=args)
    process_signal = Process_signal()
    rclpy.spin(process_signal)
    process_signal.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


    

    