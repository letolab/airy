from airy.core.db import *
from mongoengine.queryset import QuerySet

class BaseSerializer(object):
    current_level = 0
    levels = 0

    fields = ()
    exclude = ()

    def __init__(self, levels=1, fields=(), exclude=(), *args, **kwargs):
        self.levels = levels
        self.fields = fields
        self.exclude = exclude

    def to_python(self, obj):
        if isinstance(obj, QuerySet):
            return [self.to_python(item) for item in obj]

        if not obj:
            return obj

        if issubclass(obj.__class__, Document):

            return_data = []

            self.current_level += 1

            if self.levels and self.current_level > self.levels:
                return_data.append(('id', str(obj.id)))
                return_data.append(('__str__', unicode(obj)))

            else:
                for field_name in obj._fields:

                    if field_name in self.exclude:
                        continue

                    if self.fields and not field_name in self.fields:
                        continue

                    data = getattr(obj, field_name,  '')
                    field_type = obj._fields[field_name]

                    if isinstance(field_type, StringField):
                        return_data.append((field_name, unicode(data)))
                    elif isinstance(field_type, FloatField):
                        return_data.append((field_name, float(data)))
                    elif isinstance(field_type, IntField):
                        return_data.append((field_name, int(data)))
                    elif isinstance(field_type, ListField):
                        return_data.append((field_name, [self.to_python(item) for item in data]))
                    elif isinstance(field_type, ReferenceField):
                        return_data.append((field_name, self.to_python(data)))
                    else:
                        return_data.append((field_name, unicode(data)))
                        # You can define your logic for returning elements

            self.current_level -= 1

            return dict(return_data)

        return {}

    def serialize(self, queryset):
        raise NotImplementedError
