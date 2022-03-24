class IPCalculator:
    def __init__(self) -> None:
        self.class_A_mask = 0b0000 << 28
        self.class_B_mask = 0b1000 << 28
        self.class_C_mask = 0b1100 << 28
        self.class_D_mask = 0b1110 << 28
        self.class_E_mask = 0b1111 << 28
        self.private_class_A_mask = 0b00001010 << 24
        self.private_class_B_mask = 0b10101100 << 24
        self.private_class_C_mask = 0b1100000010101000 << 16

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

    @staticmethod
    def net_mask(cidr: int) -> int:
        net_mask = 0
        for i in range(cidr):
            net_mask <<= 1
            net_mask += 1
        return net_mask << (32 - cidr)

    @staticmethod
    def number_of_host(cidr: int) -> int:
        return 2 ** (32 - cidr) - 2

    def network_ip(self, ip_address: int, cidr: int) -> int:
        return ip_address & self.net_mask(cidr)

    def broadcast_ip(self, ip_address: int, cidr: int) -> int:
        return self.network_ip(ip_address, cidr) + (~self.net_mask(cidr))

    def first_host_ip(self, ip_address: int, cidr: int) -> int:
        return self.network_ip(ip_address, cidr) + 1

    def last_host_ip(self, ip_address: int, cidr: int) -> int:
        return self.broadcast_ip(ip_address, cidr) - 1

    def ip_class(self, ip_address) -> str:
        if (ip_address & self.class_E_mask) == self.class_E_mask:
            return "E"
        if (ip_address & self.class_D_mask) == self.class_D_mask:
            return "D"
        if (ip_address & self.class_C_mask) == self.class_C_mask:
            return "C"
        if (ip_address & self.class_B_mask) == self.class_B_mask:
            return "B"
        if (ip_address & self.class_A_mask) == self.class_A_mask:
            return "A"

    def ip_type(self, ip_address) -> str:
        if (ip_address & self.private_class_C_mask) == self.private_class_C_mask:
            return "Private Network"
        if (ip_address & self.private_class_B_mask) == self.private_class_B_mask:
            return "Private Network"
        if (ip_address & self.private_class_A_mask) == self.private_class_A_mask:
            return "Private Network"
        return "Public Network"


def main(class_object: IPCalculator(), ip: str, cidr: int) -> None:
    ip_int = class_object.to_number(ip)
    print("=" * 225)
    print(f"IP: {ip}")
    print(f"Binary IP: {class_object.to_binary(ip)}")
    print(f"IP Class: {class_object.ip_class(ip_int)}")
    print(f"IP Type: {class_object.ip_type(ip_int)}")
    print(f"Prefix: {cidr}")
    print(f"Netmask: {class_object.to_string(class_object.net_mask(cidr))}")
    print(f"Binary Netmask: {class_object.to_binary(class_object.to_string(class_object.net_mask(cidr)))}")
    print(f"Network Address: {class_object.to_string(class_object.network_ip(ip_int, cidr))}")
    print(f"Binary Network Address: {class_object.to_binary(class_object.to_string(class_object.network_ip(ip_int, cidr)))}")
    print(f"Subnet Broadcast Address: {class_object.to_string(class_object.broadcast_ip(ip_int, cidr))}")
    print(f"Binary Subnet Broadcast Address: {class_object.to_binary(class_object.to_string(class_object.broadcast_ip(ip_int, cidr)))}")
    print(f"First HostIP: {class_object.to_string(class_object.first_host_ip(ip_int, cidr))}")
    print(f"Binary First HostIP: {class_object.to_binary(class_object.to_string(class_object.first_host_ip(ip_int, cidr)))}")
    print(f"Last HostIP: {class_object.to_string(class_object.last_host_ip(ip_int, cidr))}")
    print(f"Binary Last HostIP: {class_object.to_binary(class_object.to_string(class_object.last_host_ip(ip_int, cidr)))}")
    print(f"Max Number Of Hosts: {class_object.number_of_host(cidr)}")
    print("=" * 225)
