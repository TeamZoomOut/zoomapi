"""Zoom.us REST API Python Client -- Chat Messages component"""

from zoomapi.util import Throttled,require_keys
from zoomapi.components import base

class ChatChannelsComponentV2(base.BaseComponent):
    """Component dealing with all chat channels related matters"""

    #List User's Channels
    @Throttled
    def list(self, **kwargs):
        return self.get_request("/chat/users/me/channels")

    #Create a Channel
    @Throttled
    def createChannel(self,**kwargs):
        require_keys(kwargs,"channel")
        return self.post_request(
            "/chat/users/me/channels",data=kwargs.get("channel")
        )


    #Get a Channel
    @Throttled
    def get(self, **kwargs):
        require_keys(kwargs,"channel_id")
        return self.get_request(
            "/chat/channels/{}".format(kwargs.get("channel_id"))
        )

    #Update a Channel (name)
    @Throttled
    def update(self,**kwargs):
        require_keys(kwargs,["channel_id","name"])
        return self.patch_request(
            "/chat/channels/{}".format(kwargs.get("channel_id")),data=kwargs.get("name")
        )

    #Delete a Channel
    @Throttled
    def delete(self,**kwargs):
        require_keys(kwargs,"channel_id")
        return self.delete_request(
            "/chat/channels/{}".format(kwargs.get("channel_id"))
        )

    #List Channel Members
    @Throttled
    def listChannelMembers(self, **kwargs):
        require_keys(kwargs, "channel_id")
        return self.get_request(
                "/chat/channels/{}/members".format(kwargs.get("channel_id"))
        ) 

    #Invite Channel Members
    @Throttled
    def inviteChannelMembers(self,**kwargs):
        require_keys(kwargs,kwargs,["channel_id","members"])
        return self.post_request(
            "/chat/channels/{}/members".format(kwargs.get("channel_id")),data=kwargs.get("members")
        )

    #Join a Channel
    @Throttled
    def joinChannel(self,**kwargs):
        require_keys(kwargs,"channel_id")
        return self.post_request(
            "/chat/channels/{}/members/me".format(kwargs.get("channel_id"))
        )

    #Leave a Channel
    @Throttled
    def leave(self, **kwargs):
        require_keys(kwargs, "channel_id")
        return self.delete_request(
            "/chat/channels/{}/members/me".format(kwargs.get("channel_id"))
        )
    
    #Remove a Member
    @Throttled
    def remove(self, **kwargs):
        require_keys(kwargs,kwargs,["channel_id","member_id"])
        return self.delete_request(
            "/chat/channels/{}/members/{}".format(kwargs.get("channel_id"),kwargs.get("member_id"))
        )

    
