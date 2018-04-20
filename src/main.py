from crawller import Crawller
from models import TapTapApp, Review, RunLog, IntegrityError
import datetime

def update_or_create(model, pk, upk, **kwargs):
    pk_value = kwargs[pk]
    try:
        obj = model.create(**kwargs)
    except IntegrityError:
        obj = model.get(getattr(model, pk) == pk_value)
        for key in upk:
            value = kwargs[key]
            setattr(obj, key, value)
        obj.save()

def crawl(appId):
    app = TapTapApp.get(TapTapApp.appId == appId)
    c = Crawller(appId)
    try:
        runlog = RunLog.get(RunLog.app == app)
        page = runlog.page
    except RunLog.DoesNotExist:
        runlog = RunLog.create(app=app, page=0)
        page = 0
    for item in c.extract_all(page):
        newPage = item['page']
        items = item['items']
        for review in items:
            reviewId = review['reviewId']
            text = review['text']
            stars = review['stars']
            update_or_create(
                Review, "reviewId", ["text", "star", ],
                app=app, text=text, star=stars, reviewId=reviewId
            )
            update_or_create(
                RunLog, "app", ["page"],
                app=app, page=newPage
            )

current = datetime.datetime.now()
crawl(72789)
print "start", current
print "end", datetime.datetime.now()
