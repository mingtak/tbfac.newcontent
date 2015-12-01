from five import grok
from plone import api
#from Products.CMFPlone.utils import safe_unicode
from Acquisition import aq_base
from zope.lifecycleevent.interfaces import IObjectModifiedEvent, IObjectAddedEvent 
from tbfac.content.article import IArticle

from zope import component
from zope.app.intid.interfaces import IIntIds
from z3c.relationfield import RelationValue
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


@grok.subscribe(IArticle, IObjectAddedEvent)
@grok.subscribe(IArticle, IObjectModifiedEvent)
def profileModify(context, event):
    if context.relatedProfile:
        return
    catalog = api.portal.get_tool(name='portal_catalog')
    brain = catalog({'Type':'Profile', 'Creator':context.owner_info()['id']})
    if not brain:
        return

    intIds = component.getUtility(IIntIds)
    profileObj = brain[0].getObject()
    context.relatedProfile = RelationValue(intIds.getId(profileObj))
    notify(ObjectModifiedEvent(context))
