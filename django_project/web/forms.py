# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

import django.forms as forms

from .models import CropField, Entry

# class aModelForm(forms.ModelForm):
#     class Meta:
#         model = aModel

#     def __init__(self, *args, **kwargs):
#         super(aModelForm, self).__init__(*args, **kwargs)


class CropFieldForm(forms.ModelForm):
    area = forms.CharField(
        widget=forms.Textarea({'hidden': ''}),
    )

    class Meta:
        model = CropField
        fields = (
            'crop_name',
            'area',
            'planting_date',
            'ph',
            'other_soil_parameters',
            'soil_texture',
            'fertilizer_use',
            'pesticide_use',
            'additional_info',
            'images'
        )


class EntryForm(forms.ModelForm):
    location = forms.CharField(
        widget=forms.Textarea({'hidden': ''}),
        required=False
    )

    class Meta:
        model = Entry
        fields = (
            'crop_field',
            'pest_disease_name',
            'entry_type',
            'occurence_date',
            'location',
            'damage_estimation',
            'is_harvested',
            'harvest_date',
            'harvest_destroyed',
            'pesticide_use',
            'additional_info',
            'images'
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)

        super(EntryForm, self).__init__(*args, **kwargs)

        crop_field_choices = [
            (c.id, c.display_name()) for c in CropField.objects.filter(
                creator=self.user
            )
        ]

        crop_field_choices.insert(0, (None, '----------'))

        self.fields['crop_field'].choices = crop_field_choices
