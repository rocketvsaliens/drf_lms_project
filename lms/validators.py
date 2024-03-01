import re
from rest_framework.serializers import ValidationError


class VideoLinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile('.*youtube\.com.*')
        tmp_val = dict(value).get(self.field)
        if tmp_val and not bool(reg.match(tmp_val)):
            raise ValidationError('Invalid video link')
