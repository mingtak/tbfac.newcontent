from five import grok
from plone.indexer import indexer

from tbfac.content import info, review, article
from tbfac.newcontent import profile, artandlife


@indexer(info.IInfo)
@indexer(review.IReview)
@indexer(article.IArticle)
@indexer(profile.IProfile)
@indexer(artandlife.IArtAndLife)
def haveImageIndexer(obj):
    if hasattr(obj, 'image'):
        return hasattr(obj.image, 'filename')
    if hasattr(obj, 'leadImage'):
        return hasattr(obj.leadImage, 'filename')
    return False
grok.global_adapter(haveImageIndexer, name="haveImage")


@indexer(artandlife.IArtAndLife)
def subjectIndexer(obj):
    keywords = []
    for i in range(len(obj.category)):
        keywords.append(obj.category[i].encode('utf-8'))
    return tuple(keywords)
grok.global_adapter(subjectIndexer, name="Subject")
