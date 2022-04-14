from flask import Flask, request
from threading import Thread
import time
import secrets

member_list = dict()
current_message = ""
app = Flask(__name__)

def encode(input, member_id = True):
  s = ""
  if member_id:
      s = "broadcastid:" + secrets.token_hex(6) + "~"
  for key, value in input.items():
    s = s + key + ":" + value + "~"
  return s[:-1]

@app.route("/")
def sendmessage():
  global current_message
  global member_list
  current_message = encode(request.args)
  for member in member_list.keys():
    member_list[member] = False
  return "how"

def broadcast(message, id = True):
  global current_message
  global member_list
  current_message = encode(message, id)
  for member in member_list.keys():
    member_list[member] = False

  return "";

@app.route("/addmember")
def add_member():
  global member_list
  global member_user_list
  id = secrets.token_hex(6)
  member_list[id] = True
  broadcast({"broadcasttype":"member_join","id":id,"username":request.args["username"]}, False)
  return id
  
@app.route("/get")
def getmessage():
  global current_message
  global member_list
  message_not_ready = request.args["id"]
  while(member_list[message_not_ready]):
    time.sleep(0.0005)
  member_list[message_not_ready] = True
  return current_message

app.run(host = '0.0.0.0',port = 8080,threaded = True)
