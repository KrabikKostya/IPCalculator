def to_number(string: str) -> int:
    res = 0
    step = 3
    for i in string.split("."):
        res += (int(i)) << (step * 8)
        step -= 1
    return res


def to_string(number: int) -> str:
    res = ["", "", "", ""]
    for i in range(4):
        res[3 - i] = str((number % 256))
        number //= 256
    return ".".join(res)


def to_binary(string: str) -> str:
    res = list(map(int, string.split('.')))
    return ".".join(list(map(lambda x: bin(x)[2:].zfill(8), res)))


class IPCalculator(object):
    def __init__(self, ip_address: str) -> None:
        self._ip_address, self._cidr = ip_address.split('/')
        self._cidr = int(self._cidr)
        self._ip_address_value = to_number(self._ip_address)
        self._net_mask = self.net_mask()
        self._network_ip = self.network_ip()
        self._broadcast_ip = self.broadcast_ip()
        self._host_range = self.host_range()

    def __str__(self) -> str:
        print("="*225)
        print(f"IP: {self._ip_address}")
        print(f"Binary IP: {to_binary(self._ip_address)}")
        print(f"IP Class: {self.ip_class()}")
        print(f"IP Type: {self.ip_type()}")
        print(f"Prefix: {self._cidr}")
        print(f"Netmask: {to_string(self._net_mask)}")
        print(f"Binary Netmask: {to_binary(to_string(self._net_mask))}")
        print(f"Network Address: {to_string(self._network_ip)}")
        print(f"Binary Network Address: {to_binary(to_string(self._network_ip))}")
        print(f"Subnet Broadcast Address: {to_string(self._broadcast_ip)}")
        print(f"Binary Subnet Broadcast Address: {to_binary(to_string(self._broadcast_ip))}")
        print(f"First HostIP: {to_string(self._host_range[0])}")
        print(f"Binary First HostIP: {to_binary(to_string(self._host_range[0]))}")
        print(f"Last HostIP: {to_string(self._host_range[1])}")
        print(f"Binary Last HostIP: {to_binary(to_string(self._host_range[1]))}")
        print(f"Max Number Of Hosts: {self.number_of_host()}")
        return "="*225

    def net_mask(self) -> int:
        net_mask = 0
        for i in range(self._cidr):
            net_mask <<= 1
            net_mask += 1
        return net_mask << (32 - self._cidr)

    def network_ip(self) -> int:
        return self._ip_address_value & self._net_mask

    def broadcast_ip(self) -> int:
        return self._network_ip + (~self._net_mask)

    def host_range(self) -> tuple:
        return self._network_ip + 1, self._broadcast_ip - 1

    def number_of_host(self) -> int:
        return 2 ** (32 - self._cidr) - 2

    def ip_class(self) -> str:
        class_A_min = to_number("1.0.0.0")
        class_A_max = to_number("126.0.0.0")
        class_B_min = to_number("128.0.0.0")
        class_B_max = to_number("191.255.0.0")
        class_C_min = to_number("192.0.0.0")
        class_C_max = to_number("223.255.255.0")
        class_D_min = to_number("224.0.0.0")
        class_D_max = to_number("239.255.255.255")
        class_E_min = to_number("240.0.0.0")
        class_E_max = to_number("247.255.255.255")
        if class_A_min < self._ip_address_value < class_A_max:
            return "A"
        elif class_B_min < self._ip_address_value < class_B_max:
            return "B"
        elif class_C_min < self._ip_address_value < class_C_max:
            return "C"
        elif class_D_min < self._ip_address_value < class_D_max:
            return "D"
        elif class_E_min < self._ip_address_value < class_E_max:
            return "E"

    def ip_type(self) -> str:
        private_class_A_min = to_number("10.0.0.0")
        private_class_A_max = to_number("10.255.255.255")
        private_class_B_min = to_number("172.16.0.0")
        private_class_B_max = to_number("172.31.255.255")
        private_class_C_min = to_number("192.168.0.0")
        private_class_C_max = to_number("192.168.255.255")
        if private_class_A_min < self._ip_address_value < private_class_A_max:
            return "Private Network"
        elif private_class_B_min < self._ip_address_value < private_class_B_max:
            return "Private Network"
        elif private_class_C_min < self._ip_address_value < private_class_C_max:
            return "Private Network"
        else:
            return "Public Network"


if __name__ == '__main__':
    print(IPCalculator("220.57.154.102/25"))
    print(IPCalculator("220.57.154.102/20"))
    print(IPCalculator("220.57.154.102/8"))
