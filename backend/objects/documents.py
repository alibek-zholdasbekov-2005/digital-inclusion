from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import AccessibilityObject

@registry.register_document
class AccessibilityObjectDocument(Document):
    district = fields.ObjectField(properties={'name': fields.TextField()})
    category = fields.ObjectField(properties={'name': fields.TextField()})

    class Index:
        name = 'accessibility_objects'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = AccessibilityObject
        fields = [
            'name_ru',
            'full_legal_name',
        ]