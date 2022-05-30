import socket
import logging


class Receiver:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.output_group = []
        self.all_groups = []

    def act(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(1)
            conn, addr = s.accept()
            conn.setblocking(True)

            with conn:
                self.get_data(conn)

    def get_data(self, conn):
        print(f'connected by {conn}')
        message = b''

        while True:
            data = conn.recv(1)

            if data == b'q':
                break

            message += data

            if data == b'\n':
                message = b''
                continue

            if message[-4:] == b'[CR]':
                if self.check_message(message):
                    self.message_to_group(message)

                message = b''

        logging.info(f'00 group: {self.output_group}')
        logging.info(f'all groups: {self.all_groups}')

    def check_message(self, message):
        text = message.decode('utf-8').strip()
        prev = None
        counter = 0
        for sym in text:
            if sym == ' ' and prev != ' ':
                counter += 1
            elif sym == ' ' and prev == ' ':
                return False
            prev = sym

        if counter == 3:
            number, channel_id, time, group = text.split()
        else:
            return False

        if not number.isdigit() or not group[:2].isdigit():
            return False

        if not channel_id[0].isalpha() or not channel_id[0].isupper() or not channel_id[1].isdigit():
            return False

        if time[2] != ':' or time[5] != ':' or time[8] != '.':
            return False

        hours, minutes, seconds = time.split(':')
        ss, ms = seconds.split('.')

        if not hours.isdigit() or int(hours) >= 24:
            return False

        if not minutes.isdigit() or int(minutes) >= 60:
            return False

        if not ss.isdigit() or int(ss) >= 60:
            return False

        if not ms.isdigit() or int(ms) >= 1000:
            return False

        return True

    def message_to_group(self, message):
        if message[-6:-4] == b'00':
            text = message.decode('utf-8')
            number, channel_id, time, group = text.split()
            time = time[:10]
            print(f'спортсмен, нагрудный номер {number} прошёл отсечку {channel_id} в «{time}»')
            self.output_group.append(message)

        self.all_groups.append(message)
        logging.info(message.decode('utf-8'))
