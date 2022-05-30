from receiver import Receiver
import logging


logging.basicConfig(filename='app_log.txt',
                    filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

host = '127.0.0.1'
port = 23
example = b'0002 C1 01:13:02.887 00[CR]'

receiver = Receiver(host, port)
receiver.act()
