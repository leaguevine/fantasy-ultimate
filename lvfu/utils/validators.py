from django.core.exceptions import ValidationError


def choice_validator(choices):
    base_choices = [t[0] for t in choices]

    def _validator(value):
        if value not in base_choices:
            raise ValidationError(u'%s is not a valid choice' % value)
    return _validator
