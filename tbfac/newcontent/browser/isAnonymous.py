from five import grok
from zope.interface import Interface
from plone import api


class IsAnonymous(grok.View):

    grok.context(Interface)
    grok.require("zope2.View")
    grok.name("isAnonymous")

    def update(self):
        self.isAnonymous = api.user.is_anonymous()
        return

    def render(self):
        return self.isAnonymous

