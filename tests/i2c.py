class I2C():

    def __init__(self, interfaceNo):
        self.interfaceNo = interfaceNo

    def readfrom_mem(self, address, register, bytes):
        self.address = address
        self.register = register
        self.bytes = bytes

    def writeto_mem(self, address, register, register_bytes):
        self.address = address
        self.register = register
        self.register_bytes = register_bytes
