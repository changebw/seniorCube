import socket

def make_connection() -> socket.socket:
    ip = '192.168.4.1' #ip of esp8266-01 module when using home wifi
    # ip = '172.20.10.6' #ip when using iphone hotspot
    port = 80 #port used in esp setup
    
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    conn.settimeout(5) # set timeout so program doesn't hang when cant connect to device

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
    conn.send("scramble".encode())

def send_solve(conn: socket.socket):
    if conn == "err":
        return
    conn.send("solve".encode())
    
def close_connection(conn):
    if conn == "err":
        return
    conn.close()

# conn = make_connection()

# for i in range(10):
#     send_scramble(conn)

# close_connection(conn)