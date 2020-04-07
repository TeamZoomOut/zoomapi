#Project Milestone - 1
#Bot program to test the api calls related to chat channels and chat messages
import sys, os
filename = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(1, filename)
from zoomapi import OAuthZoomClient

import json
from configparser import ConfigParser
from pyngrok import ngrok

parser = ConfigParser()
parser.read("bots/bot.ini")
client_id = parser.get("OAuth", "client_id")
client_secret = parser.get("OAuth", "client_secret")
port = parser.getint("OAuth", "port", fallback=4001)
browser_path = parser.get("OAuth", "browser_path")
print(f'id: {client_id} secret: {client_secret} browser: {browser_path}')

redirect_url = ngrok.connect(port, "http")
print("Redirect URL is", redirect_url)

client = OAuthZoomClient(client_id, client_secret, port, redirect_url, browser_path)
user_response = client.user.get(id='me')
user = json.loads(user_response.content)
print(user)
print ('--------------------------------------------------------------------------------------')

#create channel - should i keep the channel type as 1 default?
print("Create new channel")
name = input("Enter channel name: ")
print("Type of channel\n1. Private Channel - members must be invited to join a channel\n2. Private channel - members must be invited and should be of the same organization\n3. Public channel")
channelType = input("Enter type of channel: ")
emailList = []
stop = False
i=0
# can add 5 members at a time as per Zoom API 
while not stop:
    email = input("Enter mail id: ")
    emailDict = dict({"email":email})
    emailList.append(emailDict)
    i=i+1
    if i==5:
        stop=True
    else:
        reply=input("Do you wish to invite one more member?(y/n): ")
        if(reply=="n"):
            stop=True


channelDict = dict({"name":name,"type":channelType,"members":emailList})
zid = json.loads(client.chat_channels.createChannel(channel=channelDict).content)["id"]
print("Channel id: ",zid)
print ('--------------------------------------------------------------------------------------')

#invite members to the channel - can add 5 members at a time as per Zoom API 
emailList = []
print("Invite new members to the channel")
stop = False
i=0
while not stop:
    email = input("Enter mail id: ")
    emailDict = dict({"email":email})
    emailList.append(emailDict)
    i=i+1
    if i==5:
        stop=True
    else:
        reply=input("Do you wish to invite one more member?(y/n): ")
        if(reply=="n"):
            stop=True

memberDict = dict({"members":emailList})
output = client.chat_channels.inviteChannelMembers(channel_id=zid,members=memberDict)
print(output)
print ('--------------------------------------------------------------------------------------')

#List channel members
print("Getting list of members in the channel ",zid)
members = json.loads(client.chat_channels.listChannelMembers(channel_id=zid).content)["members"]
for m in members:
    print(m["email"])
print ('--------------------------------------------------------------------------------------')

#update channel name
print("Updating channel name of the channel ",zid)
name = input("Enter new name: ")
nameDict = dict({"name":name})
output = client.chat_channels.update(channel_id=zid,name=nameDict)
print(output)
print ('--------------------------------------------------------------------------------------')

#get channel details
print("Getting channel details for channel ",zid)
channel = json.loads(client.chat_channels.get(channel_id=zid).content)
print("Name: ",channel["name"],", Type: ",channel["type"])
print ('--------------------------------------------------------------------------------------')

#delete channel
response = input("Do you want to delete the channel?(y/n): ")
if(response == "y"):
    print("Deleting channel with id: ",zid)
    output = client.chat_channels.delete(channel_id=zid)
    print(output)
