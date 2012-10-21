from airy.core.db import *
from mongoengine.queryset import QuerySet

class BaseSerializer(object):
    def to_python(self, obj):
        if isinstance(obj, QuerySet):
            return [self.to_python(item) for item in obj]

        if not obj:
            return obj

        if issubclass(obj.__class__, Document):

            return_data = []

            for field_name in obj._fields:

                data = getattr(obj, field_name,  '')
                field_type = obj._fields[field_name]

                if isinstance(field_type, StringField):
                    return_data.append((field_name, str(data)))
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

            return dict(return_data)

        return None
