#Project Milestone - 1
#Bot program to test the api calls related to chat channels and chat messages
import sys, os
filename = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(1, filename)
from zoomapi import OAuthZoomClient

import json
from configparser import ConfigParser
from pyngrok import ngrok

import time

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
user_id=user["id"]
print ('--------------------------------------------------------------------------------------')

#List user's channel
print("User's current channel list")
channels = json.loads(client.chat_channels.list().content)["channels"]
for c in channels:
    print(c["name"]," ")
print ('--------------------------------------------------------------------------------------')

#create channel
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
cid = json.loads(client.chat_channels.createChannel(channel=channelDict).content)["id"]
print("Channel Id: ",cid)
print ('--------------------------------------------------------------------------------------')

#invite members to the channel - can add 5 members at a time as per Zoom API 
emailList = []
print("Invite new members to the channel ",cid)
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
output = client.chat_channels.inviteChannelMembers(channel_id=cid,members=memberDict)
print ('--------------------------------------------------------------------------------------')

#List channel members
print("Getting list of members in the channel ",cid)
members = json.loads(client.chat_channels.listChannelMembers(channel_id=cid).content)["members"]
for m in members:
    print(m["email"])
print ('--------------------------------------------------------------------------------------')

#update channel name
print("Updating channel name of the channel ",cid)
name = input("Enter new name: ")
nameDict = dict({"name":name})
output = client.chat_channels.update(channel_id=cid,name=nameDict)
print ('--------------------------------------------------------------------------------------')

#get channel details
print("Getting channel details for channel ",cid)
channel = json.loads(client.chat_channels.get(channel_id=cid).content)
print("Name: ",channel["name"],", Type: ",channel["type"])
print ('--------------------------------------------------------------------------------------')

#send a chat message
message = input("Enter message: ")
mId = json.loads(client.chat_messages.post(to_channel=cid, message=message).content)["id"]
print("Message sent to Channel ",cid)
print ('--------------------------------------------------------------------------------------')

#list user's chat messages
print("Listing messages sent to Channel ",cid)
print("For User ID: ",user_id)
time.sleep(2)
messages = json.loads(client.chat_messages.list(user_id=user_id,to_channel=cid).content)["messages"]
for m in messages:
    print(m["sender"],':',m["message"])
print ('--------------------------------------------------------------------------------------')
    
#update a chat message
message = input("Enter updated message for the above message: ")
output = client.chat_messages.update(messageID=mId,to_channel=cid, message=message)
print("Message updated in Channel ",cid)
print ('--------------------------------------------------------------------------------------')
time.sleep(3)

#delete a message
print("Deleting the above message...")
time.sleep(3)
output = client.chat_messages.delete(messageID=mId,to_channel=cid)
print("Message deleted in Channel ",cid)
print ('--------------------------------------------------------------------------------------')
time.sleep(3)

#remove a member
print("Remove a member from the Channel ",cid)
emailId= input("Email to remove:")
output = client.chat_channels.remove(member_id=emailId,channel_id=cid)
print("Removed member")
print ('--------------------------------------------------------------------------------------')
time.sleep(3)

#leave a channel
print("Channel id: ",cid)
print("Leaving the channel...")
time.sleep(3)
output = client.chat_channels.leave(channel_id=cid)
print("Left channel with id: ",cid)
print ("The admin powers are given to the existing members!")
print ('--------------------------------------------------------------------------------------')
time.sleep(4)

#join a channel
print("Channel id: ",cid)
print("Joining the channel...")
time.sleep(3)
output = client.chat_channels.joinChannel(channel_id=cid)
print("Joined channel with id: ",cid)
print ('--------------------------------------------------------------------------------------')
time.sleep(3)

#create channel
print ("You are not the admin anymore for the above channel.")
print("Let's create new channel to test deleting!")
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
cid = json.loads(client.chat_channels.createChannel(channel=channelDict).content)["id"]
print("Channel id: ",cid)
print ('--------------------------------------------------------------------------------------')
time.sleep(3)

#delete a channel
print("Channel id: ",cid)
print("Deleting the channel...")
time.sleep(2)
output = client.chat_channels.delete(channel_id=cid)
print("Deleted channel with id: ",cid)
time.sleep(3)
