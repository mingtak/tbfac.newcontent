from five import grok
from zope.interface import Interface
from plone import api


class CurrentUserId(grok.View):

    grok.context(Interface)
    grok.require("zope2.View")
    grok.name("currentUserId")

    def update(self):
        if api.user.is_anonymous():
            return
        self.currentUserId = api.user.get_current().id

    def render(self):
        return self.currentUserId

