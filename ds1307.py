# ds1307
DATETIME_REG = 0  # 0x00-0x06
CHIP_HALT = 128  # 或 0x80 表示(binary) 1000 0000 
ADDR = 0x68 # 或 104 表示(binary) 0110 1000

class DS1307(object):
    """Driver for the DS1307 RTC."""
    def __init__(self, i2c, addr=ADDR):
        self.i2c = i2c
        self.addr = addr
        self._halt = False
        self.weekday_start = 1

    def _dec2bcd(self, value):
        """Convert decimal to binary coded decimal (BCD) format"""
        return (value // 10) << 4 | (value % 10)

    def _bcd2dec(self, value):
        """Convert binary coded decimal (BCD) format to decimal"""
        return ((value >> 4) * 10) + (value & 0x0F)

    def get_time(self):
        buf = self.i2c.readfrom_mem(self.addr, DATETIME_REG, 7)
        return (
            self._bcd2dec(buf[6]) + 2000,  # year
            self._bcd2dec(buf[5]),  # month
            self._bcd2dec(buf[4]),  # day
            self._bcd2dec(buf[3] - self.weekday_start),  # weekday
            self._bcd2dec(buf[2]),  # hour
            self._bcd2dec(buf[1]),  # minute
            self._bcd2dec(buf[0] & 0x7F),  # second
            0  # subseconds
        )

    def set_time(self, datetime=None):
        buf = bytearray(7)
        buf[0] = self._dec2bcd(datetime[6]) & 0x7F  # second, msb = CH, 1=halt, 0=go
        buf[1] = self._dec2bcd(datetime[5])  # minute
        buf[2] = self._dec2bcd(datetime[4])  # hour
        buf[3] = self._dec2bcd(datetime[3] + self.weekday_start)  # weekday
        buf[4] = self._dec2bcd(datetime[2])  # day
        buf[5] = self._dec2bcd(datetime[1])  # month
        buf[6] = self._dec2bcd(datetime[0] - 2000)  # year
        if self._halt:
            buf[0] |= (1 << 7)
        self.i2c.writeto_mem(self.addr, DATETIME_REG, buf)

    def check_halt(self):
        """check status"""
        return self._halt

    def set_halt(self, val=None):
        """Power up or power down"""
        reg = self.i2c.readfrom_mem(self.addr, DATETIME_REG, 1)[0] # 1xxx xxxx 或 0xxx xxxx
        if val:
            reg |= CHIP_HALT # 与 1000 0000 按位或运算 -> 1xxx xxxx
        else:
            reg &= ~CHIP_HALT # 与 0111 1111 按位与运算 -> 0xxx xxxx
        self._halt = bool(val) # bool(None)==False
        self.i2c.writeto_mem(self.addr, DATETIME_REG, bytearray([reg]))