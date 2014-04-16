#!/usr/bin/pythonRoot
# bring in the libraries   
from flup.server.fcgi import WSGIServer 
from SSS-Library import *
from threading import Thread
import subprocess
import time
import Image
import socket
import sys
import os
import urlparse
import cgi
import cgitb
import thread
import random
import multiprocessing

m = multiprocessing.Manager()

myQueue = m.Queue()

def print_receipt(menu):

  printer = SSS-Library("/dev/ttyAMA0", 115200, timeout=5)

  printer.justify('C')

  # Print header
  printer.printImage(Image.open('document/receipt_header.png'), True)

  # Print the first time
  string_to_print = ""

  # Print time
  string_to_print+=str(os.popen('date +"%B %d, %Y - %R"').read())
  string_to_print+=str("\n")  
  
  # Print menu
  string_to_print+=str(menu)
  
  # Print Wifi information
  string_to_print+=str("Wifi: SSS Air Lounge\n")
  string_to_print+=str("Password: tudainhatcuatiengviet\n")
  string_to_print+=str("\n")  
  string_to_print+=str("Check-in and play our game\n")

  printer.println(string_to_print) 

  # # Print header
  # printer.printImage(Image.open('document/receipt_footer_test.png'), True)

  # Print random footer (sudoku)
  dir = 'document/receipt_footer_random/'
  randomDir = random.choice(os.listdir(dir))
  path1 = os.path.join(dir, randomDir)
  randomImg = random.choice(os.listdir(path1))
  path2 = os.path.join(path1, randomImg)
  printer.printImage(Image.open(path2), True)

  # Print fun facts:
  printer.println(facts())

  # Cut paper (full cut)
  printer.cutPaper()

  # Print the second time for archiving
  string_to_print_2=""
  string_to_print_2+=str("\n")
  string_to_print_2+=str(os.popen('date +"%B %d, %Y - %R"').read())
  string_to_print_2+=str(menu)
  printer.println(string_to_print_2)
  printer.cutPaper()

  # Print the third time for preparing
  printer.println(string_to_print_2)
  printer.cutPaper()


  printer.reset()

def addQueue(k):
  myQueue.put(k)

# all of our code now lives within the app() function which is called for each http request we receive
def app(environ, start_response):

  # start our http response 
  start_response("200 OK", [("Content-Type", "text/html")])

  # Process POST Request
  # output =
  form = cgi.FieldStorage(
    fp      = environ['wsgi.input'],
    environ = environ
  )
  k = (form['menu'].value)

  addQueue(k)

  yield "OK"

#by default, Flup works out how to bind to the web server for us, so just call it with our app() function and let it get on with it
def input_loop(myQueue):
  while True:
    if not myQueue.empty():
        val = myQueue.get()
        print_receipt(val)

# Print facts at the end
def facts():
	lines = open('document/facts.txt').read().splitlines()
	longLine =random.choice(lines)
	# print(longLine)
	totalWords = sum(1 for word in longLine.split())
	wordPerLine = 10
	repeatLine = int(totalWords/wordPerLine)+1
	# print repeatLine
	countRepeatLine=0
	wordToPrint=''
	lineToPrint='\n' + "FACTS" + '\n' 
	count=0
	# print(longLine.split())
	for i in range (0, repeatLine-1):
		for j in range(wordPerLine*i, wordPerLine*(i+1)):
			wordToPrint+=longLine.split()[j]+' '
		lineToPrint+=wordToPrint + "\n"
		wordToPrint=''
	for h in range(wordPerLine*(repeatLine-1), totalWords):
		wordToPrint+=longLine.split()[h]+' '	
	lineToPrint+=wordToPrint + "\n"
	wordToPrint=''
	return lineToPrint

t1 = Thread(target=input_loop, args=[myQueue])
t1.setDaemon(True)
t1.start()

WSGIServer(app).run()
