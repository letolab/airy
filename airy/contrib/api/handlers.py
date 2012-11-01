from airy.core.web import *
from airy.core.db import *
from airy.core.serializers.json import JSONSerializer

class APIHandler(AiryRequestHandler):
    model = Document
    serializer = JSONSerializer
    fields = set()
    exclude = set()
    levels = 1

    def get_filter_query(self):
        arguments = self.get_flat_arguments()
        use_fields = self.fields if self.fields else arguments.keys()
        use_fields = set(use_fields) - set(self.exclude)
        query_dict = dict((field, arguments[field]) for field in use_fields)
        return Q(**query_dict)

    def get_queryset(self, id=None):
        try:
            if id:
                queryset = self.model.objects.filter(self.get_filter_query()).get(id=id)
            else:
                queryset = self.model.objects.filter(self.get_filter_query())
        except Exception, e:
            if settings.debug:
                raise
            logging.warn("API Error: %s" % e)
            queryset = None
        return queryset

    def serialize(self, queryset):
        try:
            return self.serializer(levels=self.levels).serialize(queryset)
        except ValidationError, e:
            logging.warn("API Error: %s" % e)
            if settings.debug:
                return "API Error: %s" % e
            else:
                return ''

    def get(self, id=None):
        queryset = self.get_queryset(id)
        self.set_header("Content-Type", "application/json")
        self.write(self.serialize(queryset))
        self.finish()

    def put(self, id=None):
        queryset = self.get_queryset(id)
        if queryset:
            queryset.update(**self.get_flat_arguments())
        self.set_header("Content-Type", "application/json")
        self.write(self.serialize(queryset))
        self.finish()

    def post(self, id=None):
        if id:
            queryset = self.get_queryset(id)
            if queryset:
                queryset.update(**self.get_flat_arguments())
        else:
            queryset = self.model(**self.get_flat_arguments())
            if queryset:
                queryset.save()
        self.set_header("Content-Type", "application/json")
        self.write(self.serialize(queryset))
        self.finish()

    def delete(self, id=None):
        queryset = self.get_queryset(id)
        if queryset:
            queryset.delete()
        self.set_header("Content-Type", "application/json")
        self.write(self.serialize(queryset))
        self.finish()