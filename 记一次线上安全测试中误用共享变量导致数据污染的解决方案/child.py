import threading

from parent import Parent, ParentContext, ParentLocal


class Child(Parent):
    def __init__(self, args):
        super().__init__(args)
        self.port = args.get("port")

    def scan(self):
        print(threading.current_thread().name, self.all_open_ports, "id:", id(self.all_open_ports))
        self.check_port(self.port)
        pass


class ChildLocal(ParentLocal):
    def __init__(self, args):
        super().__init__(args)
        self.port = args.get("port")

    def scan(self, port=None):
        self.check_port(port or self.port)
        pass


class ChildContext(ParentContext):
    def __init__(self, args):
        super().__init__(args)
        self.port = args.get("port")

    def scan(self, port=None):
        self.check_port(port or self.port)
        pass
