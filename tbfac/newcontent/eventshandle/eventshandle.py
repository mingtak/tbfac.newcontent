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
    userRoles = user.getRoles()
    username = safe_unicode(user.getProperty('fullname'))

    if 'ArtAndLife' not in userRoles:
        return

    folderPath = "/taishin/art_and_life/%s" % userId
    catalog = portal.portal_catalog
    if len(catalog(path=folderPath)) > 0:
        return

    with api.env.adopt_user(user=user):
        with api.env.adopt_roles(['Manager']):
            folder = api.content.create(container=container, type="Folder", id=userId, title=username)
            api.content.transition(obj=folder, transition='publish')
            folder.reindexObjectSecurity()
