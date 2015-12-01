from five import grok
from zope.interface import Interface
from plone import api


class ZZZZZ(grok.View):

    grok.context(Interface)
    grok.require("zope2.View")
    grok.name("zzzzz")

    def render(self):
        context = self.context
        catalog = context.portal_catalog

        users = api.user.get_users()

        for user in users:
            currentUser = user.getUser()

            with api.env.adopt_user(user=currentUser):
                with api.env.adopt_roles(['Manager']):

                    profile = catalog({'Type':'Profile', 'id':'index_html', 'Creator':user.getId()})
                    if profile:
                        continue

                    userFolderBrain = catalog({'Type':'Folder', 'id':user.getId()})
                    if not userFolderBrain:
                        continue
                    userFolder = userFolderBrain[0].getObject()

                    try:
                        api.content.transition(obj=userFolder, transition='publish')
                    except:pass

                    try:
                        userProfile = api.content.create(
                            container=userFolder,
                            type="tbfac.newcontent.profile",
                            id="index_html",
                            title=currentUser.getProperty("fullname")
                        )
                        userProfile.manage_permission('Copy or Move', roles=['Manager', 'Site Administrator'], acquire=False)
                        api.content.transition(obj=userProfile, transition='publish')
                    except:pass
        return
