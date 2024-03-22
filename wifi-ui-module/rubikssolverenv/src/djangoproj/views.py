from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from djangoproj.wificonnect import *
from django.views.decorators.csrf import get_token
import serial,time

# def closeConnection(request):
#     close_connection(conn)
#     return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

# def takeNewPicture(request):
#     bytes_data = listen_for_image(conn)
#     convert_bytes_to_image(bytes_data)
#     close_connection(conn)
#     return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

def index(request):
    csrf_token = get_token(request)
    return render(request, 'index.html', {'csrf_token': csrf_token})

def sendScramble(request):

    # TODO: Implement the scramble

    # CONNECT TO ESP32 MOTOR CONTROLLER
    conn = make_connection("motors")
    # TODO: CALL BRADEN's SCRAMBLE ALGORITHM
    # TODO: IF NOT ALREADY PARSED, CALL PARSING FUNCTION
    # SEND STRING DATA for scramble algorithm and DISCONNECT
    send_scramble(conn)

    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

def sendSolve(request):

    # CONNECT TO ESP32 CAM 1
    conn = make_connection("cam1")

    # SEND REQUEST FOR IMAGE
    conn.send("GET /camera HTTP/1.1\r\n".encode())

    # WAIT FOR IMAGE DATA TO BE RECEIVED AND DISCONNECT
    byte_data = listen_for_image(conn)

    # SAVE IMAGE IN BACKEND AS BMP file
    convert_and_save_image(byte_data)



    # CONNECT TO ESP32 CAM 2
    conn = make_connection("cam2")

    # SEND REQUEST FOR IMAGE
    conn.send("GET /camera HTTP/1.1\r\n".encode())

    # WAIT FOR IMAGE DATA TO BE RECEIVED AND DISCONNECT
    byte_data = listen_for_image(conn)
    
    # SAVE IMAGE IN BACKEND AS BMP file
    convert_and_save_image(byte_data)

    # CONNECT TO ESP32 MOTORS
    conn = make_connection("motors")
    # TODO: CALL BRADEN's SCRAMBLE ALGORITHM
    # TODO: IF NOT ALREADY PARSED, CALL PARSING FUNCTION
    # SEND STRING DATA for scramble algorithm
    send_solve(conn)
    # DISCONNECT

    # TODO: TELL CV that the image is ready

    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

def startTimerConnection(request):
    global timerConn
    timerConn = make_connection("timer")
    if timerConn == "err": 
        print("Failed to establish connection with ESP","timer")
        status = 500 # Internal Server Error
    else: 
        status = 200 # OK
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""",status=status)

def getTime(request):
    rec_data = listen_for_time(timerConn)#user's time received from esp8266-01
    data = {
        'yourTime' : rec_data,
        'robotTime' : 'hellofromdjango',
    }
    return JsonResponse(data)