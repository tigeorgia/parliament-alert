from django import forms
from parliament.apps.alerts.models import ParliamentAlert
from parliament.apps.categories.models import Category

class AlertForm(forms.ModelForm):
    class Meta:
        model = ParliamentAlert
        fields = ('text_en','text_ka','categories','is_important')
        widgets = {
            'text_en': forms.Textarea(attrs={'cols':40, 'rows': 12}),
            'text_ka': forms.Textarea(attrs={'cols':40, 'rows': 12}),
        }

class SendAlertForm(forms.Form):
#    text = forms.CharField(widget=forms.TextInput(attrs={"readonly":True}))
#    categories = forms.ModelMultipleChoiceField(Category.objects.all(),
#        widget=forms.SelectMultiple(attrs={"readonly":True}))
#    is_important = forms.BooleanField(widget=forms.CheckboxInput(attrs={"readonly":True}))
#    language = forms.ChoiceField(ParliamentAlert.LANG_CHOICES,widget=forms.Select(attrs={"readonly":True}))
    null=forms.Field(label="",widget=forms.HiddenInput())
