'''
多功能
keyes
https://www.keyesrobot.cn/

'''
from microbit import *
import machine
import LCD1602
import TM1637

tm = TM1637.TM1637(clk=pin14, dio=pin13)
val = LCD1602.LCD1602()
display.off()
n = 0

class Servo:
    def __init__(self, pin, freq=50, min_us=600, max_us=2400, angle=180):
        self.min_us = min_us
        self.max_us = max_us
        self.us = 0
        self.freq = freq
        self.angle = angle
        self.analog_period = 0
        self.pin = pin
        analog_period = round((1/self.freq) * 1000)  # hertz to miliseconds
        self.pin.set_analog_period(analog_period)

    def write_us(self, us):
        us = min(self.max_us, max(self.min_us, us))
        duty = round(us * 1024 * self.freq // 1000000)
        self.pin.write_analog(duty)
        sleep(100)
        self.pin.write_analog(0)

    def write_angle(self, degrees=None):
        if degrees is None:
            degrees = math.degrees(radians)
        degrees = degrees % 360
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self.angle
        self.write_us(us)

Servo(pin10).write_angle(0)
while True:
    # 超声波测距
    val.puts(str(n), 0, 1)
    pin9.write_digital(0)
    sleep(0.002)
    pin9.write_digital(1)
    sleep(0.015)
    pin9.write_digital(0)

    t = machine.time_pulse_us(pin8, 1, 35000)
    if (t <= 0 and lastEchoDuration >= 0) :
        t = lastEchoDuration
    else:
        lastEchoDuration = t

    distance = int(t * 0.017)
    val.clear()
    val.puts(str(distance), 3, 0)
    val.puts("v1:", 0, 0)
    val.puts("cm", 6, 0)

    # 数码管显示声音传感器
    v4 = pin0.read_analog()
    tm.number(v4)

    # 光控灯
    val.puts("v2:", 9, 0)
    val.puts(str(pin1.read_analog()), 12, 0)
    if pin1.read_analog() > 800:
        pin3.write_digital(1)
    else:
        pin3.write_digital(0)

    # 水位警报
    val.puts("v3:", 9, 1)
    val.puts(str(pin4.read_analog()), 12, 1)
    if pin4.read_analog() > 350:
        pin2.write_digital(1)
    else:
        pin2.write_digital(0)

    # 人体红外控制舵机
    if pin10.read_digital() == 1:

        Servo(pin12).write_angle(65)

        val.puts("Someone", 0, 1)

    else:
        Servo(pin12).write_angle(0)
        val.puts("unmanned", 0, 1)

    sleep(1000)
    val.clear()
