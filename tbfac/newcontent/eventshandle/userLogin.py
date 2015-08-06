from five import grok
from plone import api
#from Products.CMFPlone.utils import safe_unicode

from Products.PlonePAS.events import UserLoggedInEvent


@grok.subscribe(UserLoggedInEvent)
def userLogin(event):
    userId = event.object.getId()
    user = api.user.get(username=userId)
    roles = api.user.get_roles(user=user)
    if "Advisor" in roles or "Guider" in roles or "Writer" in roles:
        user.setMemberProperties({'wysiwyg_editor': 'TinyMCE'})
    else:
        user.setMemberProperties({'wysiwyg_editor': 'CKeditor'})
