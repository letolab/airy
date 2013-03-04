from airy.core.web import *
from airy.core.db import *
from airy.core.serializers.json import JSONSerializer

def expose_method(f):
    def wrapped(self, *args, **kwargs):
        if f.__name__ in self.methods:
            return f(self, *args, **kwargs)
        else:
            self.write("Method Not Available")
            self.finish()
    return wrapped

class APIHandler(AiryRequestHandler):
    model = Document
    serializer = JSONSerializer
    fields = set()
    exclude = set()
    levels = 1
    methods = ('get', 'post', 'put', 'delete')

    def __init__(self, *args, **kwargs):
        super(APIHandler, self).__init__(*args, **kwargs)

        if not self.fields:
            self.fields = set(self.model._fields.keys())

    def _generate_model(self, **kwargs):
        model_fields = {}
        for key, value in kwargs.items():
            field = self.model._fields.get(key, None)
            if field:
                if isinstance(field, ReferenceField):
                    value = field.document_type.objects.get(pk=value)
                model_fields[key] = value
        return self.model(**model_fields)

    def check_xsrf_cookie(self):
        pass

    def deserialize_query(self, query_dict):
        for field_name in query_dict:
            field = self.model._fields.get(field_name)
            if isinstance(field, BooleanField):
                query_dict[field_name] = bool(query_dict[field_name])
            if isinstance(field, IntField):
                query_dict[field_name] = int(query_dict[field_name])

        return query_dict

    def get_filter_query(self):
        arguments = self.get_flat_arguments()
        use_fields = set(self.fields) & set(arguments.keys())
        use_fields = set(use_fields) - set(self.exclude)
        query_dict = dict((field, arguments[field]) for field in use_fields)
        query_dict = self.deserialize_query(query_dict)
        return Q(**query_dict)

    def get_queryset(self, id=None):
        try:
            if id:
                queryset = self.model.objects.get(id=id)
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
            return self.serializer(levels=self.levels, fields=self.fields, exclude=self.exclude).serialize(queryset)
        except ValidationError, e:
            logging.warn("API Error: %s" % e)
            if settings.debug:
                return "API Error: %s" % e
            else:
                return ''

    @report_on_fail
    @expose_method
    def get(self, id=None):
        queryset = self.get_queryset(id)
        self.set_header("Content-Type", "application/json")
        self.write(self.serialize(queryset))
        self.finish()

    @report_on_fail
    @expose_method
    def put(self, id=None):
        queryset = self.get_queryset(id)
        if queryset:
            queryset.update(**dict([("set__%s" % key, value) for key, value in self.get_flat_arguments().items()]))
        self.set_header("Content-Type", "application/json")
        self.write(self.serialize(queryset))
        self.finish()

    @report_on_fail
    @expose_method
    def post(self, id=None):
        if id:
            queryset = self.get_queryset(id)
            if queryset:
                queryset.update(**dict([("set__%s" % key, value) for key, value in self.get_flat_arguments().items()]))
        else:
            queryset = self._generate_model(**self.get_flat_arguments())
            if queryset:
                queryset.save()
        self.set_header("Content-Type", "application/json")
        self.write(self.serialize(queryset))
        self.finish()

    @report_on_fail
    @expose_method
    def delete(self, id=None):
        queryset = self.get_queryset(id)
        if queryset:
            queryset.delete()
        self.set_header("Content-Type", "application/json")
        self.write(self.serialize(queryset))
        self.finish()