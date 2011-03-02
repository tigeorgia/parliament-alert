from rapidsms.contrib.ajax.utils import call_router
import json

def _m2m2array(alert):
    return json.dumps(tuple([x for x in alert.categories.all().values_list('id')[0]]))

# access app.py via ajax router
def send_alert(alert):
    return call_router("alerts", "send_alert",
        **{ "text": alert.text,
            "categories": _m2m2array(alert),
            "is_important": unicode(alert.is_important),
            "language": alert.language,
            "id": unicode(alert.id)})
