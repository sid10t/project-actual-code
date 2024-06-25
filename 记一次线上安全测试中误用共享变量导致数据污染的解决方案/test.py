import time
import random
import threading

from child import Child, ChildContext, ChildLocal


def test_thread():
    c1 = Child({"port": 3001, "open_ports": [22, 3000, 3306]})
    t1 = threading.Thread(target=c1.scan, name="Child_1")
    t1.start()
    t1.join()

    c2 = Child({"port": 5001, "open_ports": [80, 3306, 5000]})
    t2 = threading.Thread(target=c2.scan, name="Child_2")
    t2.start()
    t2.join()

    print("All tasks have finished!")


def test_init_set():
    c1 = Child({"port": 3001, "open_ports": [22, 3000, 3306]})
    c2 = Child({"port": 3002, "open_ports": [80, 443, 3306]})
    print("c1:", c1.all_open_ports, "c2:", c2.all_open_ports)
    c1.scan()
    print("c1:", c1.all_open_ports, "c2:", c2.all_open_ports)
    c2.scan()
    print("c1:", c1.all_open_ports, "c2:", c2.all_open_ports)


def test_contextvars(open_ports, port):
    c1 = ChildContext({"port": port, "open_ports": open_ports})
    c1.scan()


def generate_random_numbers(n):
    array = []
    for _ in range(n):
        random_number = random.randint(8000, 9999)
        array.append(random_number)
    return array


def tset_local(open_ports, port):
    c1 = ChildLocal({"port": port, "open_ports": open_ports})
    c1.scan()
    args = {"port": generate_random_numbers(1)[0], "open_ports": generate_random_numbers(3)}
    print(threading.current_thread().name, args)
    c2 = ChildLocal(args)
    c2.scan()
    time.sleep(3)
    c1.scan(random.randint(8000, 9999))


if __name__ == '__main__':
    t1 = threading.Thread(target=test_contextvars, name="Child_1", args=([80, 3306, 5000], 5001,))
    t2 = threading.Thread(target=test_contextvars, name="Child_2", args=([22, 3306, 6000], 6001,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
