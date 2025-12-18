from microbit import *
from microbit import uart

while True:
    if button_a.was_pressed():
        uart.write('A')
    if button_b.was_pressed():
        uart.write('B')
    if uart.any():
        sleep(100)
        a = str(uart.readline(),"utf-8")
        if (a == '('):
            display.show(Image.SAD)
        else:
            if (a == ')'):
                display.show(Image.HAPPY)
            else:
                if (a == '-'):
                    display.show(Image.SURPRISED)
                else:
                    if (len(a) > 1):
                        display.scroll(str(a))
                    else:
                        display.show(a)

