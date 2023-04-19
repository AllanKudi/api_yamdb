from django.core.exceptions import ValidationError
from django.utils import timezone
import re


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            ('Использовать имя "me" в качестве username запрещено.'),
            params={'value': value},
        )
    if re.match(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value):
        return value
    raise ValidationError(
         'нельзя использовать недопустимые символы',
    )


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            ('Год %(value)s больше текущего!'),
            params={'value': value},
        )