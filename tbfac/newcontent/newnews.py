from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget, AutocompleteFieldWidget
from tbfac.content.info import IInfo

from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog

from tbfac.newcontent import MessageFactory as _


def back_references(source_object, attribute_name):
    """Return back references from source object on specified attribute_name.
    """
    catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    result = []
    for rel in catalog.findRelations(
                   dict(to_id=intids.getId(aq_inner(source_object)),
                        from_attribute=attribute_name)
               ):
        obj = intids.queryObject(rel.from_id)
        if obj is not None and checkPermission('zope2.View', obj):
            result.append(obj)
    return result


class INewNews(form.Schema, IImageScaleTraversable):
    """
    New News-Item contnet type
    """
    form.widget(info_ref=AutocompleteMultiFieldWidget)
    info_ref = RelationList(
        title=_(u"Related 'Info' content type"),
        value_type=RelationChoice(
            source=ObjPathSourceBinder(
                object_provides=IInfo.__identifier__,
            ),
        ),
        required=False,
    )

    info_rvw = schema.TextLine(
        title=_(u"Reviewed Info"),
        description=_(u"Use comma to separate multiple Info data."),
        required=False,
    )


class NewNews(Container):
    grok.implements(INewNews)


class SampleView(grok.View):
    """ sample view class """

    grok.context(INewNews)
    grok.require('zope2.View')
    grok.name('view')

    def relatedInfos(self):
        infos = []
        if self.context.info_ref is not None:
            for ref in self.context.info_ref:
                obj = ref.to_object
                infos.append({
                    'title': obj.title,
                })
        return infos

    def findBackReferences(self):
        backReferences = list()
        if self.context.info_ref is None:
            return backReferences
        for i in range(len(self.context.info_ref)):
            backReferences += back_references(self.context.info_ref[i].to_object, 'info_ref')
        backReferences = list(set(backReferences))
        for i in range(len(backReferences)-1, -1, -1):
            if self.context == backReferences[i]:
                backReferences.pop(i)
        return backReferences
