"""Zoom.us REST API Python Client -- Chat Messages component"""

from zoomapi.util import Throttled,require_keys
from zoomapi.components import base

class ChatChannelsComponentV2(base.BaseComponent):
    """Component dealing with all chat channels related matters"""

    @Throttled
    def list(self, **kwargs):
        return self.get_request("/chat/users/me/channels")

    #create a channel
    @Throttled
    def createChannel(self,**kwargs):
        require_keys(kwargs,"channel")
        return self.post_request(
            "/chat/users/me/channels",data=kwargs.get("channel")
        )


    #get a channel
    @Throttled
    def get(self, **kwargs):
        require_keys(kwargs,"channel_id")
        return self.get_request(
            "/chat/channels/{}".format(kwargs.get("channel_id"))
        )

    #update a channel name
    @Throttled
    def update(self,**kwargs):
        require_keys(kwargs,["channel_id","name"])
        return self.patch_request(
            "/chat/channels/{}".format(kwargs.get("channel_id")),data=kwargs.get("name")
        )

    #delete a channel
    @Throttled
    def delete(self,**kwargs):
        require_keys(kwargs,"channel_id")
        return self.delete_request(
            "/chat/channels/{}".format(kwargs.get("channel_id"))
        )

    #list channel members
    @Throttled
    def listChannelMembers(self, **kwargs):
        require_keys(kwargs, "channel_id")
        return self.get_request(
                "/chat/channels/{}/members".format(kwargs.get("channel_id"))
        ) 

    #invite channel members
    @Throttled
    def inviteChannelMembers(self,**kwargs):
        require_keys(kwargs,kwargs,["channel_id","members"])
        return self.post_request(
            "/chat/channels/{}/members".format(kwargs.get("channel_id")),data=kwargs.get("members")
        )
