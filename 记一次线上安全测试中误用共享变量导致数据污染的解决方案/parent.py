import time
import threading
import contextvars


class Parent:
    all_open_ports = set()

    def __init__(self, args):
        self.all_open_ports = set()
        self.all_open_ports.update(args.get("open_ports", []))

    def check_port(self, port):
        # 忽略端口扫描...
        if port not in self.all_open_ports:
            self.all_open_ports.add(port)
            print(f"{port} in all_open_ports, {self.all_open_ports}")


def print_prefix():
    return f"[{time.strftime('%H:%M:%S', time.localtime())} {threading.current_thread().name}]"


class ParentLocal:
    local = threading.local()

    def __init__(self, args):
        self.local.all_open_ports = getattr(self.local, "all_open_ports", set())
        self.local.all_open_ports.update(args.get("open_ports", []))

    def check_port(self, port):
        if port not in self.local.all_open_ports:
            self.local.all_open_ports.add(port)
            print(f"{print_prefix()} Port {port} is added to all_open_ports, {self.local.all_open_ports}")


class ParentContextOld:
    all_open_ports = contextvars.ContextVar("all_open_ports", default=set())

    def __init__(self, args):
        open_ports = self.all_open_ports.get()
        open_ports.update(args.get("open_ports", []))
        self.all_open_ports.set(open_ports)

    def check_port(self, port):
        all_open_ports_ = self.all_open_ports.get()
        print(print_prefix(), id(all_open_ports_))
        if port not in all_open_ports_:
            all_open_ports_.add(port)
            self.all_open_ports.set(all_open_ports_)
            print(f"{print_prefix()} Port {port} is added to all_open_ports, {self.all_open_ports.get()}")


class ParentContext:
    all_open_ports = contextvars.ContextVar("all_open_ports", default=set())

    def __init__(self, args):
        open_ports = set(args.get("open_ports", []))
        self.all_open_ports.set(open_ports | self.all_open_ports.get())

    def check_port(self, port):
        all_open_ports_ = self.all_open_ports.get()
        print(print_prefix(), id(all_open_ports_))
        if port not in all_open_ports_:
            all_open_ports_.add(port)
            self.all_open_ports.set(all_open_ports_)
            print(f"{print_prefix()} Port {port} is added to all_open_ports, {self.all_open_ports.get()}")
