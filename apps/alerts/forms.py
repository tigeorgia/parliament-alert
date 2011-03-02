from django import forms
from parliament.apps.alerts.models import ParliamentAlert
from parliament.apps.categories.models import Category

class AlertForm(forms.ModelForm):
    class Meta:
        model = ParliamentAlert
        fields = ('text','categories','is_important','language')

class SendAlertForm(forms.Form):
#    text = forms.CharField(widget=forms.TextInput(attrs={"readonly":True}))
#    categories = forms.ModelMultipleChoiceField(Category.objects.all(),
#        widget=forms.SelectMultiple(attrs={"readonly":True}))
#    is_important = forms.BooleanField(widget=forms.CheckboxInput(attrs={"readonly":True}))
#    language = forms.ChoiceField(ParliamentAlert.LANG_CHOICES,widget=forms.Select(attrs={"readonly":True}))
    null=forms.Field(label="",widget=forms.HiddenInput())
