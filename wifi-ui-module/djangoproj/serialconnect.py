import serial
import time

# Connects the board to the server
def makeConnection():
    commPort = '/dev/cu.usbmodem14301'
    try: ser = serial.Serial(commPort, baudrate=9600, timeout=1)
    except Exception:
        print("no arduino connected")
        ser = "0"
    return ser

# Turns on the LED
def turnOnLED(ser):
    if (ser != "0"):
        ser.write(b'1')

# Turns off the LED
def turnOffLED(ser):
    if (ser != "0"):
        ser.write(b'0')


## old views
# def sendHighSig(request):
#     ser = makeConnection()
#     turnOnLED(ser)
#     return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

# def sendLowSig(request):
#     ser = makeConnection()
#     turnOffLED(ser)
#     return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")
