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
from collective import dexteritytextindexer
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid
from zope.security import checkPermission
from plone import api

from tbfac.newcontent import MessageFactory as _


@grok.provider(IContextSourceBinder)
def availableType(context):
    return ObjPathSourceBinder(Type=["Info", "Article", "Review"])(context)

def checkEmail(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise Invalid(_(u"Invalid email address."))
    return True


class IProfile(form.Schema, IImageScaleTraversable):
    """
    Member's profile content type
    """

    dexterity.write_permission(specialTitle='cmf.ManagePortal')
    specialTitle = schema.TextLine(
        title=_(u'Special Title'),
        description=_(u'Special title, editable as admin'),
        required=False,
    )

    leadImage = NamedBlobImage(
        title=_(u"Persional image."),
        required=False,
    )

    # Fieldset for funlog switch on/off
    """
#    form.fieldset(
        'blogSwitch',
        label=_(u"Blog switch"),
        fields=['blogOnOff']
    )
    """

    email = schema.TextLine(
        title=_(u"email"),
        description=_(u"Contact email address"),
        required=False,
        constraint=checkEmail
    )

    """
#    form.omitted('fbLongTermToken')
#    fbLongTermToken = schema.TextLine(
        title=_(u"Facebook long term token"),
        required=False,
    )
    """

    form.omitted('collect')
    collect = RelationList(
        title=_(u'Collect'),
        description=_(u'Collection content'),
        value_type=RelationChoice(title=_(u"Collect"),
            source=availableType),
        required=False,
    )


class Profile(Container):
    grok.implements(IProfile)


class SampleView(grok.View):
    """ sample view class """

    grok.context(IProfile)
    grok.require('zope2.View')
    grok.name('view')

    def get_current(self):
        return api.user.get_current()
            

    def has_permission(self, permission, user, obj):
        if api.user.is_anonymous():
            return False
        if user.getId() == 'admin':
            return True
        return api.user.has_permission(permission, user=user, obj=obj)

    def checkPermission(self, permissionString):
        return checkPermission(permissionString, self.context)

    def getBrain(self):
        context = self.context
        catalog = context.portal_catalog
        ownerId = context.owner_info()['id']
        brain =  catalog({'Creator':ownerId,
                          'Type':['Info', 'Review', 'Article', 'ArtAndLife', 'Quarterly']},
                         sort_on='created', sort_order='reverse')
        return brain

    def toLocalizedTime(self, time, long_format=None, time_only=None):
        """Convert time to localized time
        """
        util = api.portal.get_tool(name='translation_service')
        return util.ulocalized_time(time, long_format, time_only, self.context, domain='plonelocales')


