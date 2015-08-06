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


from tbfac.newcontent import MessageFactory as _

from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog

from tbfac.content.info import IInfo
from collective import dexteritytextindexer
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget

# Interface class; used to define content-type schema.

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

def checkImage(image):
    if image._width != 230 or image._height != 230:
        raise Invalid(_(u"Constraints size: 230X230 px"))
    return True


class IArtAndLife(form.Schema, IImageScaleTraversable):
    """
    Art and Life Article
    """

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Title"),
    )

    category = schema.List(
        title=_(u'Category'),
        value_type=schema.Choice(
            values=[_(u'Month Talk'), _(u'Novel'), _(u'Body and Soul'),]
        ),
        required=True,
    )

    image = NamedBlobImage(
        title=_(u"Lead Image"),
        description=_(u"help_leadImage",
                      u"Upload a Image of Size 230x230."),
        required=False,
        constraint=checkImage,
    )

#    form.widget(info_ref=AutocompleteMultiFieldWidget)
    info_ref = RelationList(
        title=_(u"Referenced Info"),
        description=_(u"help_ReferencedInfo",
                      u"If no referenced Info items to select, please manually fill them in the next field."),
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

    dexteritytextindexer.searchable('text')
    text = RichText(
        title=_(u"text"),
        required=False,
    )


class ArtAndLife(Container):
    grok.implements(IArtAndLife)


class SampleView(grok.View):
    """ sample view class """

    grok.context(IArtAndLife)
    grok.require('zope2.View')
    #grok.name('view')

    # Add view methods here
