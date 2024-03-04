import socket
import time
from PIL import Image
from io import BytesIO
import numpy as np

def make_connection() -> socket.socket:
    # ip = '192.168.1.165'#ip when using home network
    ip = '172.20.10.9'#ip when using iphone hotspot
    port = 80 #port used in esp setup
    
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    conn.settimeout(10) # set timeout so program doesn't hang when cant connect to device

    try: 
        conn.connect((ip,port)) # try to connect
    except TimeoutError or OSError:
        print("no connection") # fail conditions
        conn.close()
        return "err"
    
    return conn

def send_scramble(conn: socket.socket):
    if conn == "err":
        return
    conn.send("scramble\0".encode())
    # time.sleep(1000)
    # close_connection(conn)

def send_solve(conn: socket.socket):
    if conn == "err":
        return
    conn.send("solve\0".encode())
    # conn.
    # close_connection(conn)
    
def close_connection(conn):
    if conn == "err":
        return
    conn.close()


def receiveTextViaSocket(conn):
    encoded = conn.recv(20)
    if not encoded:
        print("error, recieved None")
        return None
    msg = encoded.decode('utf-8')
    print("Received msg: ", msg)
    encodedAck = bytes('text_received','utf-8')
    conn.sendall(encodedAck)
    
def listen_for_image(conn):
    conn.send("GET /camera".encode())
    part = conn.recv(50)
    print(f"{part}\n\n\n")
    while 'donesetup' not in part.decode('ISO-8859-1'):
        part = conn.recv(50)
        print(f"{part}\n\n\n")        
    print(part)
    bytes_data = conn.recv(2048)
    part = bytes_data
    i = 1
    print("START IMAGE\n\n")
    while 'sent' not in part.decode('ISO-8859-1'):
        print(f"{part}\n\n\n")
        part = conn.recv(2048)
        bytes_data += part 
        i += 1
    return bytes_data

def convert_bytes_to_image(byte_data):
    byte_stream = BytesIO(byte_data)
    image = Image.frombuffer('RGB', (160, 120), byte_stream.read(), 'raw', 'BGR;16', 0, 1)
    # image.save("output.bmp", format="BMP")
    image.save("./djangoproj/media/output.bmp", format="BMP")
    # image.show()

### uncomment for debugging receive image

# conn = make_connection()
# conn.send("GET /camera".encode())


# byte_data = listen_for_image(conn)
# convert_bytes_to_image(byte_data)

# conn.close()

### uncomment for debugging send message

# while True:
#     msg = receiveTextViaSocket(conn)
#     print("received: " + str(msg))

# for i in range(10):
#     send_scramble(conn)

# close_connection(conn)