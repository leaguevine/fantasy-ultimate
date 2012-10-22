import json

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.conf import settings

from fields import JSONDateEncoder


class JSONFormField(forms.Field):
    """
    A form field that shows JSON as JSON.
    Useful to show JSON in the admin when using utils.fields.JSONField.
    """
    widget = forms.Textarea

    def prepare_value(self, value):
        return JSONDateEncoder(indent=4).encode(value)

    def to_python(self, value):
        "Returns encoded JSON."
        if value in validators.EMPTY_VALUES:
            return u''
        try:
            return json.loads(value, encoding=settings.DEFAULT_CHARSET)
        except ValueError, e:
            raise ValidationError("Invalid JSON: " + str(e))
