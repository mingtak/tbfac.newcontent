from five import grok
from zope.interface import Interface
from plone import api

from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog

from z3c.relationfield import RelationValue
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


def back_references(source_object, attribute_name):
    """Return back references from source object on specified attribute_name.
    """
    catalog = getUtility(ICatalog)
    intIds = getUtility(IIntIds)
    result = []
    for rel in catalog.findRelations(
                   dict(to_id=intIds.getId(aq_inner(source_object)),
                        from_attribute=attribute_name)
               ):
        obj = intIds.queryObject(rel.from_id)
        if obj is not None and checkPermission('zope2.View', obj):
            result.append(obj)
    return result




class Collect(grok.View):

    grok.context(Interface)
    grok.require("zope2.View")
    grok.name("collect")

    def update(self):
        if api.user.is_anonymous():
            self.collected = False
            return
        intIds = getUtility(IIntIds)
        context = self.context
        request = self.request
        response = request.response
        catalog = context.portal_catalog
        self.currentUserId = api.user.get_current().id

        brain = catalog({'Type':'Profile', 'Creator':self.currentUserId})
        if not brain:
            self.collected = False
            return
        profile = brain[0].getObject()

        if getattr(request, 'action', None) == 'add':
            if not hasattr(profile.collect, 'append'):
                profile.collect = [RelationValue(intIds.getId(context))]
                notify(ObjectModifiedEvent(profile))
                response.redirect(context.absolute_url())
                return

            for related_item in profile.collect:
                if context == related_item.to_object:
                    return
            profile.collect.append(RelationValue(intIds.getId(context)))
            notify(ObjectModifiedEvent(profile))
            response.redirect(context.absolute_url())
        elif getattr(request, 'action', None) == 'del':
            for item in profile.collect:
                if context == item.to_object:
                    profile.collect.remove(item)
                    notify(ObjectModifiedEvent(profile))
                    response.redirect(context.absolute_url())
                    break


    def render(self):
        return


class Collected(grok.View):

    grok.context(Interface)
    grok.require("zope2.View")
    grok.name("collected")

    def update(self):
        if api.user.is_anonymous():
            self.collected = False
            return
        context = self.context
        catalog = context.portal_catalog
        self.currentUserId = api.user.get_current().id

        brain = catalog({'Type':'Profile', 'Creator':self.currentUserId})
        if not brain:
            self.collected = False
            return
        profile = brain[0].getObject()

        whoCollect = back_references(context, 'collect')

        if profile in whoCollect:
            self.collected = True
        else:
            self.collected = False
        return

    def render(self):
        return self.collected
