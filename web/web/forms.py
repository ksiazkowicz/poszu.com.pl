# -*- coding: utf-8 -*-
from django import forms
from database.models import Item

class NewItemForm(forms.ModelForm):
    class Meta:
        fields = ('name','email','description','photo','is_lost','location', 'location_lat', 'location_lon', 'hash', "photo" )
        model = Item
        
    def __init__(self, *args, **kwargs):
        is_lost = kwargs.pop('is_lost')
        
        initial = {}
        initial["is_lost"] = is_lost

        super(NewItemForm, self).__init__(*args, initial=initial, **kwargs)
        # hide fields
        self.fields["location_lat"].widget = forms.HiddenInput()
        self.fields["location_lon"].widget = forms.HiddenInput()
        self.fields["is_lost"].widget = forms.HiddenInput()
        
        self.fields["name"].widget = forms.TextInput(attrs={"class": "form-control"})
        self.fields["email"].widget = forms.EmailInput(attrs={"class": "form-control"})
        #self.fields["location"].widget = forms.TextInput(attrs={"class": "osmfield osmfield-input form-control", "data-lat-field":"location_lat", "data-lon-field":"location_lon", "id": "id_location"})