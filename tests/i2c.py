class I2C():

    def __init__(self, interfaceNo):
        self.interfaceNo = interfaceNo
        self._read_result = {}
        self._read_arguments = {}
        self._write_arguments = {}

    def set_readfrom_mem_result(self, register, result_bytes):
        self._read_result[register] = result_bytes

    def readfrom_mem(self, address, register, bytes):
        self._read_arguments[register] = [address, register, bytes]
        return self._read_result[register]

    def get_readfrom_mem_arguments(self, register):
        return self._read_arguments[register]

    def writeto_mem(self, address, register, register_bytes):
        self._write_arguments[register] = [address, register_bytes]

    def get_writeto_mem_arguments(self, register):
        return self._write_arguments[register]
