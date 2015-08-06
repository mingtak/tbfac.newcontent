# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from tbfac.content.info import IInfo
from plone.app.layout.viewlets.interfaces import IAboveContent
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api


class Collect_IAboveContent_IInfo(grok.Viewlet):
    grok.viewletmanager(IAboveContent)
    grok.context(IInfo)
    grok.require('zope2.View')
    template = ViewPageTemplateFile('template/collect.pt')

    def isAnonymous(self):
        return api.user.is_anonymous()

    def render(self):
        return self.template()
