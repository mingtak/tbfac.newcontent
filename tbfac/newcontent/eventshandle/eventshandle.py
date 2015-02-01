from plone import api
from Products.CMFPlone.utils import safe_unicode
from AccessControl.SecurityManagement import getSecurityManager


def checkRoles(event):
    portal = api.portal.get()
    container = portal["art_and_life"]
    user = event.object
    if user is None:
        return
    userId = user.getId()
    user = api.user.get(userid=userId)
    userRoles = user.getRoles()
    username = safe_unicode(user.getProperty('fullname'))

    if 'ArtAndLife' not in userRoles:
        user.setMemberProperties({'wysiwyg_editor': 'CKeditor'})
        with api.env.adopt_user(username="root"):
            folderPath = "/taishin/art_and_life/%s" % userId
            folder = api.content.get(path=folderPath)
            folder.setConstrainTypesMode(1)
            folder.setLocallyAllowedTypes(('Image', 'tbfac.newcontent.artandlife'))
            folder.manage_setLocalRoles(userId, ['Member'])
            folder.reindexObjectSecurity()
        return

    user.setMemberProperties({'wysiwyg_editor': 'TinyMCE'})
    folderPath = "/taishin/art_and_life/%s" % userId
    catalog = portal.portal_catalog
    if len(catalog(path=folderPath)) > 0:
        with api.env.adopt_user(username="root"):
            folder = api.content.get(path=folderPath)
            folder.setConstrainTypesMode(1)
            folder.setLocallyAllowedTypes(('Image', 'tbfac.newcontent.artandlife'))
            folder.manage_setLocalRoles(userId, ['Contributor', 'Editor', 'Reviewer', 'Member'])
            folder.reindexObjectSecurity()
        return

    with api.env.adopt_user(username="root"):
        folder = api.content.create(container=container, type="Folder", id=userId, title=username)
        api.content.transition(obj=folder, transition='publish')
        folder.setConstrainTypesMode(1)
        folder.setLocallyAllowedTypes(('Image', 'tbfac.newcontent.artandlife'))
        folder.manage_setLocalRoles(userId, ['Contributor', 'Editor', 'Reviewer', 'Member'])
        folder.reindexObjectSecurity()
