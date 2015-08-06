from five import grok
from plone import api
from Products.CMFPlone.utils import safe_unicode

from Products.PlonePAS.events import UserInitialLoginInEvent


@grok.subscribe(UserInitialLoginInEvent)
def checkRoles(event):
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
