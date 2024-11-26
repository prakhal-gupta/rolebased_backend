from rest_framework import serializers
from rest_framework.utils import html
from rest_framework.fields import empty
from django.db import models
from django.db.models import query
from django.core.exceptions import ObjectDoesNotExist


class QuerySetSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        iterable = data.all() if isinstance(data, (models.Manager, query.QuerySet)) else data
        if isinstance(data, query.QuerySet):
            child = self.child
            meta = getattr(child, 'Meta', None)
            embeddable_fields = [fieldname for fieldname, field in child.fields.items() if isinstance(field, ModelSerializer) and field.is_embeddable()]
            select_related_fields = getattr(meta, 'select_related_fields', [])
            select_related_fields = embeddable_fields + list(select_related_fields)
            iterable = iterable.select_related(*select_related_fields)
        return [
            self.child.to_representation(item) for item in iterable
        ]


class ModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # The default for ModelSerializer is to embed the values
        self.always_embed = kwargs.pop("always_embed", True)
        super(ModelSerializer, self).__init__(*args, **kwargs)
        self.error_messages.update({
            'incorrect_type': 'Incorrect type. Expected id value, received {data_type}.',
        })

    @classmethod
    def many_init(cls, *args, **kwargs):
        child_serializer = cls(*args, **kwargs)
        list_kwargs = {'child': child_serializer}
        list_kwargs.update(dict([
            (key, value) for key, value in kwargs.items()
            if key in serializers.LIST_SERIALIZER_KWARGS
        ]))
        meta = getattr(cls, 'Meta', None)
        list_serializer_class = getattr(meta, 'list_serializer_class', QuerySetSerializer)
        return list_serializer_class(*args, **list_kwargs)

    def is_embeddable(self):
        if self.always_embed is True:
            return True
        request = self.context.get('request', None)
        assert request is not None, (
            "`%s` requires the request in the serializer if it is optionally embeddable"
            " context. Add `context={'request': request}` when instantiating "
            "the serializer." % self.__class__.__name__
        )

        embed_fields = request.query_params.getlist("embed")
        return self.field_name in embed_fields

    def get_value(self, dictionary):
        if self.is_embeddable():
            return super(ModelSerializer, self).get_value(dictionary)

        if html.is_html_input(dictionary):
            if self.field_name not in dictionary:
                if getattr(self.root, 'partial', False):
                    return empty
                return self.default_empty_html
            ret = dictionary[self.field_name]
            if ret == '' and self.allow_null:
                return '' if getattr(self, 'allow_blank', False) else None
            return ret
        return dictionary.get(self.field_name, empty)

    def to_internal_value(self, data):
        if self.is_embeddable():
            return super(ModelSerializer, self).to_internal_value(data)
        ModelClass = self.Meta.model
        try:
            return ModelClass.objects.get(pk=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)

    def to_representation(self, instance):
        if self.is_embeddable():
            return super(ModelSerializer, self).to_representation(instance)
        return instance.pk


class SawaggerResponseSerializer(serializers.Serializer):
   status = serializers.BooleanField(default=True)
   message = serializers.CharField()
   data = serializers.ListField(allow_empty=True)