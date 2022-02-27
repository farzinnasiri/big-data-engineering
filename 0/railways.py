import json
import random
import threading
import time
from socket import *

ONE_WAY = "ONE_WAY"
TWO_WAY = "TWO_WAY"

lock = threading.Lock()


def log(*args):
    lock.acquire()
    print(time.strftime("%I:%M:%S %p", time.localtime()), " ", *args)
    lock.release()


class Message:
    def __init__(self, train_uid, velocity, railway_uid):
        self.train_uid = train_uid
        self.velocity = velocity
        self.railway_uid = railway_uid


class Railway:
    def __init__(self, uid, length):
        self.uid = uid
        self.length = length


class Manager(threading.Thread):
    def __init__(self, port, railways, count_railways):
        super().__init__()
        self.port = port
        self.railways = railways
        self.accepting = False
        self.request = {}

        for i in range(count_railways):
            self.request[i + 1] = []

    def run(self):
        receive_socket = socket(AF_INET, SOCK_DGRAM)
        receive_socket.bind(("localhost", self.port))

        payload, _ = receive_socket.recvfrom(2048)
        self.accepting = True

        while self.accepting:
            payload, _ = receive_socket.recvfrom(2048)
            self.add_to_queue(payload)

    def add_to_queue(self, data):
        message = Message(**json.loads(data))

        self.request[message.railway_uid] \
            .append(Train(message.train_uid, message.velocity, 0, 0, 0))

    def schedule(self):
        for railway in self.request:
            log("scheduling for railway: ", railway)
            self.sort_sjf(self.request[railway], self.railways[railway].length)

    def sort_sjf(self, trains, rail_length):
        trains.sort(key=lambda x: rail_length / x.velocity)
        for train in trains:
            print(train.uid, " ")


class Train(threading.Thread):
    def __init__(self, uid, velocity, count_railways, wait_time, manager_port):
        super().__init__()
        self.uid = uid
        self.velocity = velocity
        self.count_railways = count_railways
        self.wait_time = wait_time
        self.manager_port = manager_port

    def choose_railway(self):
        railway_id = random.randrange(1, self.count_railways)
        log(self.uid, ":",railway_id)
        return railway_id

    def run(self):
        time.sleep(self.wait_time)

        railway_id = self.choose_railway()
        message = Message(self.uid, self.velocity, railway_id)

        channel = socket(AF_INET, SOCK_DGRAM)
        channel \
            .sendto(json.dumps(message.__dict__)
                    .encode("utf-8"), ("localhost", self.manager_port))


def main():
    n, m = [int(x) for x in input().split()]

    railways = {}
    for i in range(n):
        uid, length, kind = [int(x) for x in input().split()]
        railways[uid] = Railway(uid, length)

    trains = []
    for i in range(m):
        uid, velocity = [int(x) for x in input().split()]
        trains.append(Train(uid, velocity, n, 2, 8080))

    manager = Manager(8080, railways, n)
    manager.start()

    for train in trains:
        train.start()

    for train in trains:
        train.join()

    manager.schedule()


if __name__ == "__main__":
    main()
