from airy.utils import simplejson
from airy.core.serializers.base import BaseSerializer

class JSONSerializer(BaseSerializer):

    def serialize(self, queryset):
        return simplejson.dumps(super(JSONSerializer, self).to_python(queryset))
