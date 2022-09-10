from django.core.exceptions import ValidationError
def validate_length(value,length=8):
    if len(str(value))!=length:
        raise ValidationError(u'%s numero de telephone invalide dans Tunis!' % value)
