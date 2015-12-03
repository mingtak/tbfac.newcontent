from five import grok
from plone import api
from Products.CMFPlone.utils import safe_unicode

from Products.PlonePAS.events import UserInitialLoginInEvent
from Products.PlonePAS.events import UserLoggedInEvent


@grok.subscribe(UserLoggedInEvent)
def checkProfile(event):
    portal = api.portal.get()
    catalog = portal.portal_catalog
    currentUser = event.object
#    import pdb; pdb.set_trace()
    brain = catalog({'Type':'Profile', 'id':event.object.getId()})
    if brain:
        return
    with api.env.adopt_user(user=currentUser):
        with api.env.adopt_roles(['Manager']):
            userFolder = catalog({'Type':'Folder', 'id':event.object.getId()})[0].getObject()
#            api.content.transition(obj=userFolder, transition='publish')
            userProfile = api.content.create(
                container=userFolder,
                type="tbfac.newcontent.profile",
                id="index_html",
                title=currentUser.getProperty("fullname")
            )
            userProfile.manage_permission('Copy or Move', roles=['Manager', 'Site Administrator'], acquire=False)
            api.content.transition(obj=userProfile, transition='publish')

    redirectUrl = userProfile.absolute_url()
    response = event.object.REQUEST.response
    response.redirect(redirectUrl, lock=True)
    return


@grok.subscribe(UserInitialLoginInEvent)
def initialAccount(event):
    portal = api.portal.get()
    currentUser = event.object
#    import pdb; pdb.set_trace()
    with api.env.adopt_user(user=currentUser):
        with api.env.adopt_roles(['Manager']):
            userFolder = api.content.create(
                type='Folder',
                title=currentUser.getProperty("fullname"),
                id=currentUser.getUserId(),
                container=portal['juries']
            )
            api.content.transition(obj=userFolder, transition='publish')
            userProfile = api.content.create(
                container=userFolder,
                type="tbfac.newcontent.profile",
                id="index_html",
                title=currentUser.getProperty("fullname")
            )
            userProfile.manage_permission('Copy or Move', roles=['Manager', 'Site Administrator'], acquire=False)
            api.content.transition(obj=userProfile, transition='publish')

    redirectUrl = userProfile.absolute_url()
    response = event.object.REQUEST.response
    response.redirect(redirectUrl, lock=True)
    return

