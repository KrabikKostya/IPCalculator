class IPCalculator(object):
    def __init__(self, ip_address: str) -> None:
        self.ip_address, self.cidr = ip_address.split('/')
        self.cidr = int(self.cidr)
        self.ip_address_value = self.to_number(self.ip_address)
        self.net_mask = self.net_mask()
        self.network_ip = self.network_ip()
        self.broadcast_ip = self.broadcast_ip()
        self.host_range = self.host_range()

    @staticmethod
    def to_number(string: str) -> int:
        res = 0
        step = 3
        for i in string.split("."):
            res += (int(i)) << (step * 8)
            step -= 1
        return res

    @staticmethod
    def to_string(number: int) -> str:
        res = ["", "", "", ""]
        for i in range(4):
            res[3 - i] = str((number % 256))
            number //= 256
        return ".".join(res)

    @staticmethod
    def to_binary(string: str) -> str:
        res = list(map(int, string.split('.')))
        return ".".join(list(map(lambda x: bin(x)[2:].zfill(8), res)))

    def net_mask(self) -> int:
        net_mask = 0
        for i in range(self.cidr):
            net_mask <<= 1
            net_mask += 1
        return net_mask << (32 - self.cidr)

    def network_ip(self) -> int:
        return self.ip_address_value & self.net_mask

    def broadcast_ip(self) -> int:
        return self.network_ip + (~self.net_mask)

    def host_range(self) -> tuple:
        return self.network_ip + 1, self.broadcast_ip - 1

    def number_of_host(self) -> int:
        return 2 ** (32 - self.cidr) - 2

    def ip_class(self) -> str:
        class_A_min = self.to_number("1.0.0.0")
        class_A_max = self.to_number("126.0.0.0")
        class_B_min = self.to_number("128.0.0.0")
        class_B_max = self.to_number("191.255.0.0")
        class_C_min = self.to_number("192.0.0.0")
        class_C_max = self.to_number("223.255.255.0")
        class_D_min = self.to_number("224.0.0.0")
        class_D_max = self.to_number("239.255.255.255")
        class_E_min = self.to_number("240.0.0.0")
        class_E_max = self.to_number("247.255.255.255")
        if class_A_min <= self.ip_address_value <= class_A_max:
            return "A"
        elif class_B_min <= self.ip_address_value <= class_B_max:
            return "B"
        elif class_C_min <= self.ip_address_value <= class_C_max:
            return "C"
        elif class_D_min <= self.ip_address_value <= class_D_max:
            return "D"
        elif class_E_min <= self.ip_address_value <= class_E_max:
            return "E"

    def ip_type(self) -> str:
        private_class_A_min = self.to_number("10.0.0.0")
        private_class_A_max = self.to_number("10.255.255.255")
        private_class_B_min = self.to_number("172.16.0.0")
        private_class_B_max = self.to_number("172.31.255.255")
        private_class_C_min = self.to_number("192.168.0.0")
        private_class_C_max = self.to_number("192.168.255.255")
        if private_class_A_min <= self.ip_address_value <= private_class_A_max:
            return "Private Network"
        elif private_class_B_min <= self.ip_address_value <= private_class_B_max:
            return "Private Network"
        elif private_class_C_min <= self.ip_address_value <= private_class_C_max:
            return "Private Network"
        else:
            return "Public Network"


def main(ip) -> None:
    print("=" * 225)
    print(f"IP: {ip.ip_address}")
    print(f"Binary IP: {ip.to_binary(ip.ip_address)}")
    print(f"IP Class: {ip.ip_class()}")
    print(f"IP Type: {ip.ip_type()}")
    print(f"Prefix: {ip.cidr}")
    print(f"Netmask: {ip.to_string(ip.net_mask)}")
    print(f"Binary Netmask: {ip.to_binary(ip.to_string(ip.net_mask))}")
    print(f"Network Address: {ip.to_string(ip.network_ip)}")
    print(f"Binary Network Address: {ip.to_binary(ip.to_string(ip.network_ip))}")
    print(f"Subnet Broadcast Address: {ip.to_string(ip.broadcast_ip)}")
    print(f"Binary Subnet Broadcast Address: {ip.to_binary(ip.to_string(ip.broadcast_ip))}")
    print(f"First HostIP: {ip.to_string(ip.host_range[0])}")
    print(f"Binary First HostIP: {ip.to_binary(ip.to_string(ip.host_range[0]))}")
    print(f"Last HostIP: {ip.to_string(ip.host_range[1])}")
    print(f"Binary Last HostIP: {ip.to_binary(ip.to_string(ip.host_range[1]))}")
    print(f"Max Number Of Hosts: {ip.number_of_host()}")
    print("=" * 225)


if __name__ == '__main__':
    ip1 = IPCalculator("220.57.154.102/25")
    ip2 = IPCalculator("220.57.154.102/20")
    ip3 = IPCalculator("220.57.154.102/8")

    main(ip1)
    main(ip2)
    main(ip3)
