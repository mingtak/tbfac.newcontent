from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from plone.directives import form
from zope.component import adapts
from zope.interface import alsoProvides, implements
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget, AutocompleteFieldWidget
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from tbfac.content.info import IInfo
from plone.supermodel.interfaces import FIELDSETS_KEY

from tbfac.newcontent import MessageFactory as _


class IRelatedItem(model.Schema):
    """
       Marker/Form interface for RelatedItem
    """
#    form.widget(relatedItem=AutocompleteMultiFieldWidget)
    relatedItem = RelationList(
        title=_(u"Related 'Info' content type"),
        value_type=RelationChoice(
            source=ObjPathSourceBinder(
                object_provides=IInfo.__identifier__,
            ),
        ),
        required=False,
    )

fieldset = model.Fieldset('categorization', label=_(u'Categorization'), fields=['relatedItem'])
IRelatedItem.setTaggedValue(FIELDSETS_KEY, [fieldset])
alsoProvides(IRelatedItem, IFormFieldProvider)

def context_property(name):
    def getter(self):
        return getattr(self.context, name)
    def setter(self, value):
        setattr(self.context, name, value)
    def deleter(self):
        delattr(self.context, name)
    return property(getter, setter, deleter)


class RelatedItem(object):
    """
       Adapter for RelatedItem
    """
    implements(IRelatedItem)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
