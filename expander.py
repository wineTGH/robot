import smbus2 as smbus

IODIRA = 0x00  # Pin direction register
IODIRB = 0x01  # Pin direction register
IPOLA = 0x02
IPOLB = 0x03

OLATA = 0x14
OLATB = 0x15
ALL_OFFSET = [IODIRA, IODIRB, IPOLA, IPOLB, OLATA, OLATB]

GPA0 = 0
GPA1 = 1
GPA2 = 2
GPA3 = 3
GPA4 = 4
GPA5 = 5
GPA6 = 6
GPA7 = 7
GPB0 = 8
GPB1 = 9
GPB2 = 10
GPB3 = 11
GPB4 = 12
GPB5 = 13
GPB6 = 14
GPB7 = 15
ALL_GPIO = [
    GPA0,
    GPA1,
    GPA2,
    GPA3,
    GPA4,
    GPA5,
    GPA6,
    GPA7,
    GPB0,
    GPB1,
    GPB2,
    GPB3,
    GPB4,
    GPB5,
    GPB6,
    GPB7,
]

HIGH = 0xFF
LOW = 0x00

INPUT = 0xFF
OUTPUT = 0x00


class Expander:
    dev_addr: int
    bus: smbus.SMBus

    def __init__(self, dev_addr: int, i2c_addr: int):
        self.bus = smbus.SMBus(i2c_addr)
        self.dev_addr = dev_addr

    def set_all_output(self):
        self.bus.write_byte_data(self.dev_addr, IODIRA, OUTPUT)
        self.bus.write_byte_data(self.dev_addr, IODIRB, OUTPUT)

    def set_all_input(self):
        self.bus.write_byte_data(self.dev_addr, IODIRA, INPUT)
        self.bus.write_byte_data(self.dev_addr, IODIRB, INPUT)

    def write(self, pin: int, value: bool):
        pair = self.get_offset_gpio_tuple([OLATA, OLATB], pin)
        self.set_bit_enabled(pair[0], pair[1], value)

    def get_offset_gpio_tuple(self, offsets: list[int], gpio: int):
        if offsets[0] not in ALL_OFFSET or offsets[1] not in ALL_OFFSET:
            raise TypeError("offsets must contain a valid offset address. See description for help")
        if gpio not in ALL_GPIO:
            raise TypeError("pin must be one of GPAn or GPBn. See description for help")

        offset = offsets[0] if gpio < 8 else offsets[1]
        _gpio = gpio % 8
        return (offset, _gpio)

    def set_bit_enabled(self, offset: int, gpio: int, enable: bool):
        stateBefore = self.bus.read_byte_data(self.dev_addr, offset)
        value = (
            (stateBefore | self.bitmask(gpio)) if enable else (stateBefore & ~self.bitmask(gpio))
        )
        self.bus.write_byte_data(self.dev_addr, offset, value)

    def bitmask(self, gpio):
        return 1 << (gpio % 8)
