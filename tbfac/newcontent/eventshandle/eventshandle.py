from plone import api
from Products.CMFPlone.utils import safe_unicode


def setFolderState(folder, userId, rolesList, allowedTypes):
    folder.setConstrainTypesMode(1)
    folder.setLocallyAllowedTypes(allowedTypes)
    folder.manage_setLocalRoles(userId, rolesList)
    folder.reindexObjectSecurity()


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
    folderPath = "/art_and_life/%s" % userId
    folder = api.content.get(path=folderPath)

    if 'ArtAndLife' not in userRoles:
        user.setMemberProperties({'wysiwyg_editor': 'CKeditor'})
        if folder is None:
            return
        with api.env.adopt_user(username="root"):
            setFolderState(folder,
                           userId,
                           ['Member'],
                           ('Image', 'tbfac.newcontent.artandlife'))
        return

    user.setMemberProperties({'wysiwyg_editor': 'TinyMCE'})
    catalog = portal.portal_catalog
    if folder is not None:
        with api.env.adopt_user(username="root"):
            setFolderState(folder,
                           userId,
                           ['Contributor', 'Editor', 'Reviewer', 'Member'],
                           ('Image', 'tbfac.newcontent.artandlife'))
        return

    with api.env.adopt_user(username="root"):
        folder = api.content.create(container=container, type="Folder", id=userId, title=username)
        api.content.transition(obj=folder, transition='publish')
        setFolderState(folder,
                       userId,
                       ['Contributor', 'Editor', 'Reviewer', 'Member'],
                       ('Image', 'tbfac.newcontent.artandlife'))
