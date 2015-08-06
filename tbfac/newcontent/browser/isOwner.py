from five import grok
from zope.interface import Interface
from plone import api


class isOwner(grok.View):

    grok.context(Interface)
    grok.require("zope2.View")
    grok.name("isOwner")

    def update(self):
        if api.user.is_anonymous():
            self.isOwner = False

        currentUserId = api.user.get_current().id
        ownerId = self.context.owner_info()['id']
        self.isOwner = currentUserId == ownerId

    def render(self):
        return self.isOwner
