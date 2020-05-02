from typing import Union, Callable
import win32net

import wx
import wx.adv

# Message types
from qbubbles.advUtils.filesystem import File

INFO = "info"
WARN = "warn"
WARNING = "warn"
ERROR = "error"

# Connection lost types
CONN_LOST = "conn_lost"
CONN_TIMEOUT = "conn_timeout"
CONN_SUCCESS = "conn_success"

# States
STATE_LAUNCH = "state_launch"

# Connection types
CLIENT = "client"
SERVER = "server"


class _Utils:
    @staticmethod
    def remove_duplicates(list_: list) -> list:
        index = 0
        already_defined = []
        while index < len(list_):
            if already_defined:
                if list_[index] in already_defined:
                    del list_[index]
                    continue
            already_defined.append(list_[index])
            index += 1
        return list_


class Downloader(object):
    def __init__(self, url, file):
        # InfoNone
        self._url = url
        self._file = file

        # Booleans
        self.downloadActive = True

        # Integers
        self.totalDownloaded = 0
        self.fileTotalbytes = 0
        self.timeRemaining = -1

        # Strings
        self.info = ""

        # Modules
        import os
        import time
        import qbubbles.advUtils.system
        import threading
        self._os = os
        self._time = time
        self._system = qbubbles.advUtils.system
        self._threading = threading
        self.spd = 0

        # Status
        self.title = f"Initializing..."
        self.message1 = f""
        self.message2 = f""
        self.message3 = f""
        self.message4 = f""
        self.status_list = [self.title, self.message1, self.message2, self.message3, self.message4]
        self.status = str.join("\n", self.status_list)

    def speed(self):
        """
        Speed information update thread

        :return:
        """
        # Load.SetValue(int(self.totalDownloaded / self.fileTotalbytes), )
        self.info = f"Downloading...\nDownloading of \"{self._url.split('/')[-1]}\""
        while self.downloadActive:
            total1 = self.totalDownloaded
            self._time.sleep(0.45)
            total2 = self.totalDownloaded
            self.spd = (total2 - total1) * 2
            try:
                a = self.fileTotalbytes / self.spd
                b = self._time.gmtime(a)
            except ZeroDivisionError:
                a = -1
                b = self._time.gmtime(a)
            self.timeRemaining = b

    def download(self):
        import urllib.request
        h = "23"
        m = "59"
        s = "59"
        self.spd: Union[int, float] = 0
        self.totalDownloaded: int = 0

        # Get the total number of bytes of the file to download before downloading
        url_request = urllib.request.urlopen(str(self._url))
        meta: dict = url_request.info()
        if "Content-Length" in meta.keys():
            self.fileTotalbytes = int(meta["Content-Length"])
        else:
            raise KeyError(f"The url '{self._url}' has no meta named 'Content-Length'")
        if self.fileTotalbytes < 0:
            raise ValueError(f"The file at '{self._url}' has an invalid file size: {self.fileTotalbytes}")
        elif self.fileTotalbytes == 0:
            raise ValueError(f"The file at '{self._url}' is empty")

        data_blocks: list = []
        total: int = 0

        file = File(self._file)

        self._system.StoppableThread(target=lambda: self.speed(), name="SpeedThread").start()

        while True:
            block = url_request.read()
            data_blocks.append(block)
            total += len(block)
            _hash = ((60 * self.totalDownloaded) // self.fileTotalbytes)
            # Frame.Update()
            # Panel.Update()
            # Down.Update()
            _temp0002 = self._url.split('/')[-1]
            _temp0003 = str(int(self.totalDownloaded / self.fileTotalbytes * 100))

            self.title = f"Downloading..."
            self.message1 = f"Downloading of \"{_temp0002} is {_temp0003}% complete."
            self.message2 = f""
            self.message3 = f"{str(total)} of {str(self.fileTotalbytes)}"
            self.message4 = f"With {str(self.spd)} bytes/sec | {h}:{m}:{s} remaining."
            self.status_list = [self.title, self.message1, self.message2, self.message3, self.message4]
            self.status = str.join("\n", self.status_list)

            if not len(block):
                self.downloadActive = False
                break

            fd = file.open("ab")
            fd.write(block)
            fd.close()

        # data = b''.join(data_blocks)  # had to add b because I was joining bytes not strings
        url_request.close()

        # with open("C:\\Users\\" + self._os.getlogin() + "\\Downloads\\" + self._url.split("/")[-1], "wb") as f:
        #     f.write(data)

        # Frame.SetWindowStyle(wx.DEFAULT_FRAME_STYLE)
        # load.Destroy()
        # Frame.Show(True)
        notify = wx.adv.NotificationMessage(
            title="Download successful",
            message="Your download is complete!\n\nCheck out in your downloads folder.",
            parent=None, flags=wx.ICON_INFORMATION)
        notify.Show(timeout=0)  # 1 for short timeout, 100 for long timeout


class Server(object):
    "A class for a Server instance."""

    def __init__(self, port_):
        # super(Server, self).__init__(chat_text)
        self.port = port_
        # self.chatText = chat_text
        # self.network = network

        self.preInitHook: Callable = lambda server, sock1, sock2: None
        self.postInitHook: Callable = lambda server, conn, addr, secret: None

        self.conn_array = []
        self.secret_array = {}

        import math
        import random
        import socket
        import threading
        self._math = math
        self._random = random
        self._socket = socket
        self._threading = threading

        self.event: Callable = lambda evt_type, server: None

    def is_prime(self, number):
        """
        Checks to see if a number is prime.

        :param number:
        :return:
        """
        x = 1
        if number == 2 or number == 3:
            return True
        while x < self._math.sqrt(number):
            x += 1
            if number % x == 0:
                return False
        return True

    def runner(self, conn, secret):
        pass

    def run(self):
        while True:
            s = self._socket.socket(self._socket.AF_INET, self._socket.SOCK_STREAM)
            try:
                s.bind(('', self.port))
            except OSError:
                return

            if len(self.conn_array) == 0:
                self.event(CONN_SUCCESS, "server")
            s.listen(1)

            conn_init, addr_init = s.accept()
            pak_init = PackageSystem(conn_init)
            serv = self._socket.socket(self._socket.AF_INET, self._socket.SOCK_STREAM)
            serv.bind(('', 0))  # get a random empty port_

            self.preInitHook(self, s, serv)

            serv.listen(1)

            port_val = serv.getsockname()[1]
            pak_init.send(port_val)

            del pak_init
            conn_init.close()
            conn, addr = serv.accept()

            pak = PackageSystem(conn)

            self.conn_array.append(conn)  # add an array entry for this connection
            self.event(CONN_SUCCESS, self)

            # create the numbers for my encryption
            prime = self._random.randint(1000, 9000)
            while not self.is_prime(prime):
                prime = self._random.randint(1000, 9000)
            base = self._random.randint(20, 100)
            a = self._random.randint(20, 100)

            # send the numbers (base, prime, A)
            # conn.send(self.network.format_number(len(str(base))).encode())
            # conn.send(str(base).encode())
            #
            # conn.send(self.network.format_number(len(str(prime))).encode())
            # conn.send(str(prime).encode())
            #
            # conn.send(self.network.format_number(len(str(pow(base, a) % prime))).encode())
            # conn.send(str(pow(base, a) % prime).encode())
            #
            # # get B
            # data = conn.recv(4)
            # data = conn.recv(int(data.decode()))
            # b = int(data.decode())

            pak.send(base)
            pak.send(prime)
            pak.send(pow(base, a))

            b = PackageReciever(conn).recv()

            # calculate the encryption key
            secret = pow(b, a) % prime
            # store the encryption key by the connection
            self.secret_array[conn] = secret

            self.postInitHook(self, conn, addr, secret)

            self._threading.Thread(target=self.runner, args=(conn, secret)).start()
            del pak
            # # Server(self.port_).start()
        # self.start()

    def start(self):
        self._threading.Thread(target=self.run).start()


# Client chat
class Client(object):
    """
    A class for a Client instance.
    """

    def __init__(self, host, port_):
        """

        :param host:
        :param port_:
        """
        # super(Client, self).__init__(chat_text)
        self.port = port_
        self.host = host
        # self.network = network

        self.preInitHook: Callable = lambda client, conn_init2: None
        self.postInitHook: Callable = lambda client, conn, secret: None

        import socket
        import random
        import threading
        self._socket = socket
        self._random = random
        self._threading = threading

        self.secret_array = {}
        self.conn_array = []

        self.event: Callable = lambda evt_type, client: None

    def runner(self, conn, secret):
        pass

    def run(self):
        """

        :return:
        """
        conn_init2 = self._socket.socket(self._socket.AF_INET, self._socket.SOCK_STREAM)
        conn_init2.settimeout(5.0)
        pak_init = PackageSystem(conn_init2)
        try:
            conn_init2.connect((self.host, self.port))
        except self._socket.timeout:
            raise SystemExit(0)
        except self._socket.error:
            raise SystemExit(0)

        self.preInitHook(self, conn_init2)

        # Recieve port
        porte = pak_init.recv()

        del pak_init
        conn_init2.close()

        # New connection
        conn = self._socket.socket(self._socket.AF_INET, self._socket.SOCK_STREAM)
        conn.connect((self.host, porte))
        pak = PackageSystem(conn)

        self.event(CONN_SUCCESS, self)

        self.conn_array.append(conn)

        # Get my base, prime, and A values
        base = pak.recv()
        prime = pak.recv()
        a = pak.recv()
        b = self._random.randint(20, 100)
        # Send the 'b' value
        pak.send(pow(base, b) % prime)
        secret = pow(a, b) % prime

        self.secret_array[conn] = secret
        self.postInitHook(self, conn, secret)

        self._threading.Thread(target=self.runner, args=(conn, secret)).start()
        del pak
        # Server(self.port_).start()                             # Errored command! #
        # THIS IS GOOD, BUT I CAN'T TEST ON ONE MACHINE

    def start(self):
        self._threading.Thread(target=self.run).start()


class PackageEncoder(object):
    def __init__(self, data):
        self.data = data

        import pickle
        self._pickle = pickle

    def get_encoded(self):
        data = self._pickle.dumps(self.data)
        length = len(data)

        return length, data


class PackageDecoder(object):
    def __init__(self, data: bytes):
        self.data = data

        import pickle
        self._pickle = pickle

    def get_decoded(self):
        data = self._pickle.loads(self.data)

        return data


class PackageSender(object):
    def __init__(self, conn, data):
        self._length, self._data = PackageEncoder(data).get_encoded()

        import socket

        self.conn: socket.socket = conn

    def send(self):
        len_str = str(self._length)

        for _ in range(32, len(len_str), -1):
            len_str = "0" + len_str

        self.conn.send(len_str.encode())
        self.conn.send(self._data)


class PackageReciever(object):
    def __init__(self, conn):
        import socket

        self.conn: socket.socket = conn

    def recv(self):
        length = self.conn.recv(32)
        data = self.conn.recv(int(length))

        return PackageDecoder(data).get_decoded()


class PackageSystem(object):
    def __init__(self, conn):
        import socket

        self.conn: socket.socket = conn

    def send(self, o):
        length, data = PackageEncoder(o).get_encoded()

        len_str = str(length)

        for _ in range(32, len(len_str), -1):
            len_str = "0" + len_str

        # print(len(len_str))
        # print(len_str)

        self.conn.send(len_str.encode())
        self.conn.send(data)

    def recv(self):
        length = self.conn.recv(32)
        data = self.conn.recv(int(length.decode()))

        return PackageDecoder(data).get_decoded()


class CryptedPackageSystem(PackageSystem):
    def __init__(self, conn):
        super(CryptedPackageSystem, self).__init__(conn)

    @staticmethod
    def _encrypt(b, key):
        from Crypto.Cipher import ARC4

        obj = ARC4.new(key.encode())
        return obj.encrypt(b)

    @staticmethod
    def _decrypt(b, key):
        from Crypto.Cipher import ARC4

        obj2 = ARC4.new(key.encode())
        return obj2.decrypt(b)

    def send_c(self, o, key):
        _, data = PackageEncoder(o).get_encoded()
        # print(data, key)
        data = self._encrypt(data, key)
        length = len(data)

        len_str = str(length)

        for _ in range(32, len(len_str), -1):
            len_str = "0" + len_str

        # print(len(len_str))
        # print(len_str)

        self.conn.send(len_str.encode())
        self.conn.send(data)

    def recv_c(self, key):
        try:
            length = self.conn.recv(32)
            data = self.conn.recv(int(length.decode()))
        except ValueError:
            return None
        return PackageDecoder(self._decrypt(data, key)).get_decoded()


class NetworkInfo(object):
    localIPv4 = "127.0.0.1"
    localIPv6 = "::1"

    @staticmethod
    def get_external_ip(ext_ip_url='https://ident.me'):
        import urllib.request
        external_ip = urllib.request.urlopen(ext_ip_url).read().decode('utf8')
        return external_ip

    @staticmethod
    def get_internal_ip():
        import socket
        ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                           if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)),
                                                                 s.getsockname()[0], s.close()) for s in
                                                                [socket.socket(socket.AF_INET,
                                                                               socket.SOCK_DGRAM)]][0][1]]) if l][-1][0]
        return ip

    @staticmethod
    def convert2ipv6(ip4str):
        import ipaddress
        return str(ipaddress.IPv6Address(int(ipaddress.IPv4Address(ip4str))))

    @staticmethod
    def connect_wifi(ssid, password):
        raise NotImplementedError("NetworkInfo(...).connect_wifi(...) is not yet created")

    @staticmethod
    def list_wifi_ssids():
        import pywifi

        wifi = pywifi.PyWiFi()
        interfaces = wifi.interfaces()
        # print(interfaces)
        interfaces[-1].scan()
        from time import sleep
        sleep(2)
        # interfaces[0].connect()
        results = interfaces[0].scan_results()
        # print(results)
        # print(results[0].ssid)
        ssids = [result.ssid for result in results]
        print(ssids)
        ssids = _Utils.remove_duplicates(ssids)
        # print(ssids)
        return ssids

    @staticmethod
    def get_personal_shares():
        WindowsShares(NetworkInfo.get_internal_ip())

    @staticmethod
    def add_personal_share():
        raise NotImplementedError()
        # win32net.NetShareAdd()

    @staticmethod
    def get_network_interfaces():
        import pywifi

        wifi = pywifi.PyWiFi()
        interfaces = wifi.interfaces()
        return interfaces


class WindowsShares(object):
    def __init__(self, ip):
        self._ip = ip

    def get_shares(self):
        win32net.NetShareEnum(self._ip)


if __name__ == '__main__':
    # a_ = PackageSender(None, {"Hallo"})
    # a_.send()

    def c_runner(conn, secret):
        pak = PackageSystem(conn)
        for i in range(3):
            recieved = pak.recv()
            print(f"Recieved Type: {type(recieved)}")
            print(f"Recieved Data: {recieved}")
        exit(0)


    def s_runner(conn, secret):
        import random

        pak = PackageSystem(conn)
        for i in range(1):
            b = []
            for _ in range(16):
                b.append(chr(random.randint(64, 96)))
            a = f"{''.join(b)}"

            b = random.randint(-5000, +5000)
            pak.send(a)
            pak.send(b)
            pak.send(list(a))
        exit(0)

    print(f"NetworkInfo Test | Data value                                            ")
    print(f"_________________|_______________________________________________________")
    print(f"Get internal IPv6| {NetworkInfo.convert2ipv6(NetworkInfo.get_internal_ip())}")
    print(f"Get external IP  | {NetworkInfo.get_external_ip()}                       ")
    print(f"Get internal IP  | {NetworkInfo.get_internal_ip()}                       ")
    print(f"List WiFi SSIDs  | {NetworkInfo.list_wifi_ssids()}                       ")
    print(f"Network shares   | {win32net.NetShareEnum(NetworkInfo.get_internal_ip())}")
    print(f"_________________|_______________________________________________________")

    print("\nClient and Server Test")

    server_ = Server(36673)
    server_.runner = s_runner
    server_.start()
    client_ = Client("127.0.0.1", 36673)
    client_.runner = c_runner
    client_.start()
