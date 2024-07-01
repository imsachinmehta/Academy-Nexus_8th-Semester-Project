from django import forms
from .models import Room

class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "description"]
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")
        if name[0].isdigit():
            raise forms.ValidationError("Name cannot begin with a number")
        if len(name) > 15:
            raise forms.ValidationError("Name cannot be more than 15 characters!")
        if len(description) > 70:
            raise forms.ValidationError("Description cannot be more than 70 characters!")
        return cleaned_data
    
    def save(self, slugfield, creator):
        room = Room.objects.create(
            name=self.cleaned_data['name'],
            description=self.cleaned_data['description'],
            slug=slugfield,
            creator=creator
        )
        room.save()
        return room