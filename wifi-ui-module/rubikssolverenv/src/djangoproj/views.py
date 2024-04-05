from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from djangoproj.wificonnect import *
from django.views.decorators.csrf import get_token
import serial,time
# from djangoproj.algorithms.Cube import Cube
from djangoproj.CV.colorByFace import *
from djangoproj.Cube import Cube

def index(request):
    csrf_token = get_token(request)
    return render(request, 'index.html', {'csrf_token': csrf_token})

def sendScramble(request):

    # CONNECT TO ESP32 MOTOR CONTROLLER
    conn = make_connection("cam1")#TODO: change to motors later
    
    # CALL BRADEN's SCRAMBLE ALGORITHM
    cube = Cube()
    cube.printCube()
    moves = cube.randomScramble(20)
    
    # SEND STRING DATA for scramble algorithm and DISCONNECT
    send_scramble(conn, moves)

    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

def sendSolve(request):
    # CONNECT TO ESP32 CAM 1
    conn = make_connection("cam1")

    # SEND REQUEST FOR IMAGE
    conn.send("GET /camera HTTP/1.1\r\n".encode())

    # WAIT FOR IMAGE DATA TO BE RECEIVED AND DISCONNECT
    byte_data = listen_for_image(conn)

    # SAVE IMAGE IN BACKEND AS BMP file
    convert_and_save_image1(byte_data)

    print("TAKING NEXT PICTURE IN 5..")
    time.sleep(1)
    print("4..")
    time.sleep(1)
    print("3..")
    time.sleep(1)
    print("2..")
    time.sleep(1)
    print("1..")

    # CONNECT TO ESP32 CAM 2, for now use cam1 since only have one camera
    conn = make_connection("cam1")#TODO: change back to cam2 when ready

    # SEND REQUEST FOR IMAGE
    conn.send("GET /camera HTTP/1.1\r\n".encode())

    # WAIT FOR IMAGE DATA TO BE RECEIVED AND DISCONNECT
    byte_data = listen_for_image(conn)
    
    # SAVE IMAGE IN BACKEND AS BMP file
    convert_and_save_image2(byte_data)

    # RUN CV ON IMAGE AND GET FACELIST
    pixelDetector = colorByFace('./djangoproj/CV/topview.bmp','./djangoproj/CV/botview.bmp')
    faceList = pixelDetector.allFaces()

    print(faceList)

    # TODO: CALL BRADEN's SOLVE ALGORITHM ON FACELIST
    solveString = "RbBlLRFfdRBdbD"

    # CONNECT TO ESP32 MOTORS
    conn = make_connection("cam1")#TODO: change to motors later
    conn.send(solveString.encode())
    # TODO: IF NOT ALREADY PARSED, CALL PARSING FUNCTION
    # SEND STRING DATA for scramble algorithm
    # send_solve(conn)
    # DISCONNECT

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

    if rec_data == "error":
        return JsonResponse({},status=500)
    else: 
        data = {
            'yourTime' : rec_data,
            'robotTime' : rec_data,
        }
        return JsonResponse(data,status=200)

def startLearnModeConnection(request):
    print("called start learn mode")
    # CONNECT TO ESP32 CAM 1
    conn = make_connection("cam1")

    # SEND REQUEST FOR IMAGE
    conn.send("GET /camera HTTP/1.1\r\n".encode())

    # WAIT FOR IMAGE DATA TO BE RECEIVED AND DISCONNECT
    byte_data = listen_for_image(conn)

    # SAVE IMAGE IN BACKEND AS BMP file
    convert_and_save_image1(byte_data)

    print("TAKING NEXT PICTURE IN 5..")
    time.sleep(1)
    print("4..")
    time.sleep(1)
    print("3..")
    time.sleep(1)
    print("2..")
    time.sleep(1)
    print("1..")

    # CONNECT TO ESP32 CAM 2, for now use cam1 since only have one camera
    conn = make_connection("cam1")#TODO: change back to cam2 when ready

    # SEND REQUEST FOR IMAGE
    conn.send("GET /camera HTTP/1.1\r\n".encode())

    # WAIT FOR IMAGE DATA TO BE RECEIVED AND DISCONNECT
    byte_data = listen_for_image(conn)
    
    # SAVE IMAGE IN BACKEND AS BMP file
    convert_and_save_image2(byte_data)

    # RUN CV ON IMAGE AND GET FACELIST
    pixelDetector = colorByFace('./djangoproj/CV/topview.bmp','./djangoproj/CV/botview.bmp')
    faceList = pixelDetector.allFaces()

    print(faceList)

    # TODO: CALL BRADEN's SOLVE ALGORITHM ON FACELIST
    
    # GET SOLVE STRING
    # MAKE IT GLOBAL
    global solveString
    solveString = "RbBlLRFfdRBdbD"
    curr_move = solveString[0]

    match curr_move:
        case "R":
            curr_move = "Right Clockwise"
        case "r":
            curr_move = "Right Counter-Clockwise"
        case "L":
            curr_move = "Left Clockwise"
        case "l":
            curr_move = "Left Counter-Clockwise"
        case "D":
            curr_move = "Down Clockwise"
        case "d":
            curr_move = "Down Counter-Clockwise"
        case "F":
            curr_move = "Front Clockwise"
        case "f":
            curr_move = "Front Counter-Clockwise"
        case "B":
            curr_move = "Back Clockwise"
        case "b":
            curr_move = "Back Counter-Clockwise"
        case _:
            curr_move = "Invalid Move"

    data = {
            'moves': solveString,
            'curr_move': curr_move
        }

    # CONNECT TO MOTORS
    
    global learnConn

    learnConn = make_connection("cam1")#TODO: change to motors later

    if learnConn == "err": 
        print("Failed to establish connection with ESP","motors")
        status = 500 # Internal Server Error
    else: 
        status = 200 # OK
    
    return JsonResponse(data,status=200)

def sendMove(request):

    global solveString
    global learnConn
    # SEND NEXT MOVE WHEN USER CLICKS "NEXT"
    curr_move = solveString[0]
    send_move(learnConn, curr_move)
    
    # UPDATE SOLVE STRING TO GET READY FOR NEXT MOVE
    if len(solveString) > 1:
        solveString = solveString[1:]
        next_move = solveString[0]
    else:
        solveString = ""
        next_move = "DONE!"

    match next_move:
        case "R":
            next_move = "Right Clockwise"
        case "r":
            next_move = "Right Counter-Clockwise"
        case "L":
            next_move = "Left Clockwise"
        case "l":
            next_move = "Left Counter-Clockwise"
        case "D":
            next_move = "Down Clockwise"
        case "d":
            next_move = "Down Counter-Clockwise"
        case "F":
            next_move = "Front Clockwise"
        case "f":
            next_move = "Front Counter-Clockwise"
        case "B":
            next_move = "Back Clockwise"
        case "b":
            next_move = "Back Counter-Clockwise"
        case _:
            next_move = "DONE! Click Start to Restart."
    
    status = 200

    if next_move is not None:
        data = {
                'moves': solveString,
                'curr_move': next_move
            }
    else:
        data = {}
        status = 500

    return JsonResponse(data,status=status)