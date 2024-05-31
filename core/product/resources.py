# product/resources.py
from import_export import resources, fields
from .models import Standards

class CombinedStandardsResource(resources.ModelResource):
    astm_name = fields.Field(attribute='standard_astm__name', column_name='ASTM Name')
    astm_value = fields.Field(attribute='standard_astm__value', column_name='ASTM Value')
    aashto_name = fields.Field(attribute='standard_aashto__name', column_name='AASHTO Name')
    aashto_value = fields.Field(attribute='standard_aashto__value', column_name='AASHTO Value')
    isiri_name = fields.Field(attribute='standard_isiri__name', column_name='ISIRI Name')
    isiri_value = fields.Field(attribute='standard_isiri__value', column_name='ISIRI Value')

    class Meta:
        model = Standards
        fields = ('id', 'title', 'slug', 'astm_name', 'astm_value', 'aashto_name', 'aashto_value', 'isiri_name', 'isiri_value')

    def dehydrate_astm_value(self, obj):
        return obj.standard_astm.value.url if obj.standard_astm and obj.standard_astm.value else ''

    def dehydrate_aashto_value(self, obj):
        return obj.standard_aashto.value.url if obj.standard_aashto and obj.standard_aashto.value else ''

    def dehydrate_isiri_value(self, obj):
        return obj.standard_isiri.value.url if obj.standard_isiri and obj.standard_isiri.value else ''
