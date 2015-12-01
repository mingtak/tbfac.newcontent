from five import grok
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives as form
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapts
from zope.interface import Interface, alsoProvides, implements
from plone.indexer import indexer

from tbfac.newcontent import MessageFactory as _


class ISpecialTitle(model.Schema):
    """
       Marker/Form interface for SpecialTitle
    """
    form.mode(specialTitle='hidden')
    specialTitle = schema.TextLine(
        title=_(u'Special Title'),
        description=_(u'Special title, editable as admin'),
        required=False,
    )


alsoProvides(ISpecialTitle, IFormFieldProvider)

def context_property(name):
    def getter(self):
        return getattr(self.context, name)
    def setter(self, value):
        setattr(self.context, name, value)
    def deleter(self):
        delattr(self.context, name)
    return property(getter, setter, deleter)


class SpecialTitle(object):
    """
       Adapter for SpecialTitle
    """
    implements(ISpecialTitle)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    specialTitle = context_property('specialTitle')


@indexer(Interface)
def specialTitle_indexer(obj):
#    import pdb; pdb.set_trace()
    if obj.Type() == 'Profile':
        return obj.specialTitle

    catalog = obj.portal_catalog
    brain = catalog({'Type':'Profile', 'Creator':obj.owner_info()['id']})
    if not brain:
        return
#    import pdb; pdb.set_trace()
    if hasattr(obj, 'specialTitle'):
        if '++add++' in obj.REQUEST.URL:
#            import pdb; pdb.set_trace()
            profile = brain[0]
            obj.specialTitle = profile.specialTitle
            return obj.specialTitle
        else:
#            import pdb; pdb.set_trace()
            return obj.specialTitle
grok.global_adapter(specialTitle_indexer, name='specialTitle')

