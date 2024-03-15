import socket
import time
from PIL import Image
from io import BytesIO

def make_connection() -> socket.socket:
    # ip = '192.168.1.165'#ip when using home network
    # ip = '192.168.1.210'#ip when using iphone hotspot
    ip = '172.20.10.10'
    port = 80 #port used in esp setup
    
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    conn.settimeout(10) # set timeout so program doesn't hang when cant connect to device

    try: 
        conn.connect((ip,port)) # try to connect
    except TimeoutError or OSError:
        print("no connection") # fail conditions
        conn.close()
        return "err"
    
    print("success")
    
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

    size_nxt = int(conn.recv(2)) #size
    conn.recv(2) # newline chars
    
    print(size_nxt)
    part = conn.recv(size_nxt) #get msg
    conn.recv(2) # newline chars
    print(f"{part}\n\n")
    conn.send("ackResponse\r\n".encode())
    
    size_nxt = int(conn.recv(2)) #size
    conn.recv(2) # newline chars
    
    print(size_nxt)
    part = conn.recv(size_nxt) #get msg
    conn.recv(2) # newline chars
    print(f"{part}\n\n")
    conn.send("ackContentType\r\n".encode())

    size_nxt = int(conn.recv(2)) #size
    conn.recv(2) # newline chars
    
    print(size_nxt)
    part = conn.recv(size_nxt) #get msg
    conn.recv(2) # newline chars
    print(f"{part}\n\n")
    # conn.send("ackConnection\r\n".encode())

    # size_nxt = int(conn.recv(2)) #size
    # conn.recv(2) # newline chars
    
    # print(size_nxt)
    # part = conn.recv(size_nxt) #get msg
    # conn.recv(2) # newline chars
    # print(f"{part}\n\n")
    conn.send("ackSetupDone\r\n".encode())

    # size_bmp = int(conn.recv(2)) #size
    # conn.recv(2) #newline chars

    # print("size bmp head: ",size_bmp)
    # bmp_head = conn.recv(size_bmp)
    # conn.recv(2) #newline
    # print(f"{bmp_head}\n\n")
    # conn.send("ackGotBMP\r\n".encode())

    # size_img = int(conn.recv(2))
    # conn.recv(2)

    # print(print("size img: ",size_img))
    # bytes_data = conn.recv(100)
    # conn.recv(2)
    # print(f"{part}\n\n")
    # conn.send("ackGotImage".encode())


    bytes_data = conn.recv(2048)

    while True:
        part = conn.recv(2048)
        bytes_data += part
        if b'sent' in part:
            break

        bytes_data = bytes_data.replace(b'sent', b'')
    
    return bytes_data

def convert_bytes_to_image(byte_data):
    byte_stream = BytesIO(byte_data)
    try:
        image = Image.open(byte_stream)
        image.save("./djangoproj/media/output.bmp", format="BMP")
    except Exception as e:
        print("Error processing image:", e)

### uncomment for debugging receive image
conn = make_connection()
conn.send("GET /camera HTTP/1.1\r\n".encode())

byte_data = listen_for_image(conn)
convert_bytes_to_image(byte_data)

conn.close()

### uncomment for debugging send message

# while True:
#     msg = receiveTextViaSocket(conn)
#     print("received: " + str(msg))

# for i in range(10):
#     send_scramble(conn)

# close_connection(conn)