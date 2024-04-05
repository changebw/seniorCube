import socket
import time
from PIL import Image
from io import BytesIO
import random
from datetime import datetime

'''
|===== ESP32 INTERFACING INFO =====|

    ESP32 (esp_id = "cam1")
        ip = '172.20.10.9'
        port = 80
    ESP32 (esp_id = "cam2")
        ip = '172.20.10.10'
        port = 80
    ESP32 (esp_id = "motors")
        ip = '172.20.10.7'
        port = 80
    ESP8266 (esp_id = "timer")
        ip = '172.20.10.6'
        port = 8080

|==================================|    
'''

# Connect to ESP Module based on esp_id
def make_connection(esp_id: str) -> socket.socket:
    if esp_id == "cam1":
        ip = '172.20.10.9'
        port = 80
    elif esp_id == "cam2":
        ip = '172.20.10.10'
        port = 80
    elif esp_id == "motors":
        ip = '172.20.10.7'
    else:
        ip = '172.20.10.6'
        port = 8080
    
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    conn.settimeout(10) # set timeout so program doesn't hang when cant connect to device

    try: 
        conn.connect((ip,port)) # try to connect
    except TimeoutError or OSError:
        print("Unable to establish a connection with ESP, exiting...") # fail conditions
        conn.close()
        return "err"
    
    print("Successfully connected to ESP with ID =", esp_id)
    
    return conn

def send_scramble(conn: socket.socket, moves: str):
    if conn != "err":
        conn.send("POST /scramble HTTP/1.1\r\n".encode())
        print("send req")
        response_size = conn.recv(2) # size
        response = conn.recv(17)
        print("RESPONSE IS: " + str(response))
        if b'HTTP/1.1 200 OK' in response:
            print("good response")
            move_string = moves + "SENTSCRAMBLE\r\n"
            print(move_string)
            conn.send(move_string.encode())
            time.sleep(1)
        conn.close()

def send_solve(conn, moves):
    if conn != "err":
        conn.send("POST /solve HTTP/1.1\r\n".encode())
        print("send req")
        response_size = conn.recv(2) # size
        response = conn.recv(17)
        print("RESPONSE IS: " + str(response))
        if b'HTTP/1.1 200 OK' in response:
            print("good response")
            move_string = moves + "SENTSOLVE\r\n"
            print(move_string)
            conn.send(move_string.encode())
            time.sleep(1)
        conn.close()

def send_move(conn: socket.socket, move: str):
    if conn != "err":
        conn.send("POST /move HTTP/1.1\r\n".encode())
        print("send req")
        response_size = conn.recv(2) # size
        response = conn.recv(25)
        print("RESPONSE IS: " + str(response))
        if b'HTTP/1.1 200 OK' in response:
            print("good response")
            move_string = move + "SENTSOLVE\r\n"
            print(move_string)
            conn.send(move_string.encode())
            time.sleep(1)

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
    conn.send("ackSetupDone\r\n".encode())

    bytes_data = conn.recv(2048)

    while True:
        part = conn.recv(2048)
        bytes_data += part
        if b'sent' in part:
            break

    bytes_data = bytes_data.replace(b'sent', b'')

    conn.close()
    
    return bytes_data

def convert_and_save_image1(byte_data):
    byte_stream = BytesIO(byte_data)
    now = datetime.now()
    try:
        image = Image.open(byte_stream)
        # image.save(f"./djangoproj/media/output{now}.bmp", format="BMP")
        image.save(f"./djangoproj/CV/topview.bmp", format="BMP")
    except Exception as e:
        print("Error processing image:", e)

def convert_and_save_image2(byte_data):
    byte_stream = BytesIO(byte_data)
    now = datetime.now()
    try:
        image = Image.open(byte_stream)
        # image.save(f"./djangoproj/media/output{now}.bmp", format="BMP")
        image.save(f"./djangoproj/CV/botview.bmp", format="BMP")
    except Exception as e:
        print("Error processing image:", e)

def listen_for_time(conn):
    conn.send("GET /time\r\n".encode())

    encoded = ""

    try: 
        encoded = conn.recv(8)
    except (OSError,TimeoutError) as e:
        encoded = "err"
    
    msg = "error"
    
    if encoded != "err":
        msg = encoded.decode('utf-8')
    
    print("Received msg: ", msg)
    return msg



### uncomment for debugging receive image
# conn = make_connection("cam1")
# conn.send("GET /camera HTTP/1.1\r\n".encode())

# byte_data = listen_for_image(conn)
# convert_and_save_image(byte_data)

# conn.close()

### uncomment for debugging send message

# while True:
#     msg = receiveTextViaSocket(conn)
#     print("received: " + str(msg))

# for i in range(10):
#     send_scramble(conn)

# close_connection(conn)