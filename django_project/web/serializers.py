from rest_framework import serializers

from django.core.urlresolvers import reverse

from .models import (
    CropField,
    Entry
)


class CropFieldSerializer(serializers.ModelSerializer):
    url_detail = serializers.SerializerMethodField('get_detail_page_url')
    url_edit = serializers.SerializerMethodField('get_edit_page_url')
    # calls the get_number_of_incidents method. "get" is prepended by default.
    number_of_incidents = serializers.SerializerMethodField()
    creator_object = serializers.SerializerMethodField()

    class Meta:
        model = CropField
        fields = (
            'id',
            'crop_name',
            'area',
            'url_detail',
            'url_edit',
            'number_of_incidents',
            'creator_object'
        )

    def get_detail_page_url(self, obj):
        return reverse('crop-field-detail', args=[obj.pk])

    def get_edit_page_url(self, obj):
        return reverse('edit-crop-field', args=[obj.pk])

    def get_number_of_incidents(self, obj):
        return obj.entries.all().count()

    def get_creator_object(self, obj):
        return {
            'id': obj.creator.id,
            'name': obj.creator.username
        }


class IndividualEntriesSerializer(serializers.ModelSerializer):
    url_detail = serializers.SerializerMethodField('get_detail_page_url')
    url_edit = serializers.SerializerMethodField('get_edit_page_url')
    creator_object = serializers.SerializerMethodField()
    type_object = serializers.SerializerMethodField()

    class Meta:
        model = Entry
        fields = (
            'id',
            'location',
            'pest_disease_name',
            'occurence_date',
            'damage_estimation',
            'url_detail',
            'url_edit',
            'creator_object',
            'type_object'
        )

    def get_detail_page_url(self, obj):
        return reverse('entry-detail', args=[obj.pk])

    def get_edit_page_url(self, obj):
        return reverse('edit-entry', args=[obj.pk])

    def get_creator_object(self, obj):
        return {
            'id': obj.creator.id,
            'name': obj.creator.username
        }

    def get_type_object(self, obj):
        return {
            'typeId': obj.entry_type,
            'name': obj.get_entry_type_display()
        }


class CropFieldMobileSerializer(serializers.ModelSerializer):
    # calls the get_number_of_incidents method. "get" is prepended by default.
    number_of_incidents = serializers.SerializerMethodField()
    creator_object = serializers.SerializerMethodField()

    class Meta:
        model = CropField
        fields = (
            'id',
            'crop_name',
            'area',
            'number_of_incidents',
            'creator_object'
        )

    def get_detail_page_url(self, obj):
        return reverse('crop-field-detail', args=[obj.pk])

    def get_number_of_incidents(self, obj):
        return obj.entries.all().count()

    def get_creator_object(self, obj):
        return {
            'id': obj.creator.id,
            'name': obj.creator.username
        }


class IndividualEntriesMobileSerializer(serializers.ModelSerializer):
    creator_object = serializers.SerializerMethodField()
    type_object = serializers.SerializerMethodField()

    class Meta:
        model = Entry
        fields = (
            'id',
            'location',
            'pest_disease_name',
            'occurence_date',
            'damage_estimation',
            'creator_object',
            'type_object'
        )

    def get_creator_object(self, obj):
        return {
            'id': obj.creator.id,
            'name': obj.creator.username
        }

    def get_type_object(self, obj):
        return {
            'typeId': obj.entry_type,
            'name': obj.get_entry_type_display()
        }
