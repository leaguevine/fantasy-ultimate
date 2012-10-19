import datetime
import json

from django.conf import settings
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _


class JSONDateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M:%S')
        return json.JSONEncoder.default(self, obj)


class JSONField(models.TextField):
    description = _("Data that serializes and " +
                    "deserializes into and out of JSON.")

    def _dumps(self, data):
        return JSONDateEncoder().encode(data)

    def _loads(self, str):
        return json.loads(str, encoding=settings.DEFAULT_CHARSET)

    def db_type(self, connection):
        return 'text'

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        return self._dumps(value)

    def contribute_to_class(self, cls, name):
        self.class_name = cls
        super(JSONField, self).contribute_to_class(cls, name)
        signals.post_init.connect(self.post_init)

        def get_json(model_instance):
            return self._dumps(getattr(model_instance, self.attname, None))
        setattr(cls, 'get_%s_json' % self.name, get_json)

        def set_json(model_instance, json):
            return setattr(model_instance, self.attname, self._loads(json))
        setattr(cls, 'set_%s_json' % self.name, set_json)

    def post_init(self, **kwargs):
        if 'sender' in kwargs and 'instance' in kwargs:
            if (kwargs['sender'] == self.class_name and
                    hasattr(kwargs['instance'], self.attname)):
                value = self.value_from_object(kwargs['instance'])
                if (value):
                    setattr(kwargs['instance'], self.attname,
                            self._loads(value))
                else:
                    setattr(kwargs['instance'], self.attname, None)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^lvfu\.utils\.fields\.JSONField"])
