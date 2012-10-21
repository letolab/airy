from airy.core.web import *
from airy.core.db import *
from airy.core.serializers.json import JSONSerializer

class APIHandler(AiryRequestHandler):
    model = Document
    serializer = JSONSerializer

    def get_filter_query(self):
        return Q()

    def get(self, id=None):
        if id:
            queryset = self.model.objects.filter(self.get_filter_query()).get(pk=id)
        else:
            queryset = self.model.objects.filter(self.get_filter_query())
        self.set_header("Content-Type", "application/json")
        self.write(self.serializer().serialize(queryset))
        self.finish()

    def put(self, id=None):
        if id:
            queryset = self.model.objects.filter(self.get_filter_query()).get(pk=id)
        else:
            queryset = self.model.objects.filter(self.get_filter_query())
        queryset.update(**self.get_flat_arguments())

    def post(self, id=None):
        if id:
            queryset = self.model.objects.filter(self.get_filter_query()).get(pk=id)
            queryset.update(**self.get_flat_arguments())
        else:
            queryset = self.model(**self.get_flat_arguments())
            queryset.save()

    def delete(self, id=None):
        if id:
            queryset = self.model.objects.filter(self.get_filter_query()).get(pk=id)
        else:
            queryset = self.model.objects.filter(self.get_filter_query())
        queryset.delete()