from airy.core.conf import settings
from tornado.web import *


class AiryHandler(RequestHandler):
    
    def render_string(self, template_name, **kwargs):
        context_processors = getattr(settings, 'template_context_processors', [])
        template_args = {}
        for processor_path in context_processors:
            path, name = processor_path.rsplit('.', 1)
            processor_module = __import__(path, fromlist=path)
            processor = getattr(processor_module, name)
            template_args.update(processor(self, **kwargs))
        template_args.update(kwargs)
        return super(AiryHandler, self).render_string(template_name, **template_args)

