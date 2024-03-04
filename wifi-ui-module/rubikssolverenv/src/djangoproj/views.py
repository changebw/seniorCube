from django.shortcuts import render
from django.http import HttpResponse
from djangoproj.wificonnect import *
from django.views.decorators.csrf import get_token
import serial,time

def index(request):
    csrf_token = get_token(request)
    return render(request, 'index.html', {'csrf_token': csrf_token})

def makeConnection(request):
    global conn
    conn = make_connection()
    if conn == "err": response = HttpResponse("""<html><script>window.location.replace('/');</script></html>""",status=500)
    else: response = HttpResponse("""<html><script>window.location.replace('/');</script></html>""")
    return response

def sendScramble(request):
    send_scramble(conn)
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

def sendSolve(request):
    send_solve(conn)
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

def closeConnection(request):
    close_connection(conn)
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

def takeNewPicture(request):
    bytes_data = listen_for_image(conn)
    convert_bytes_to_image(bytes_data)
    close_connection(conn)
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")
