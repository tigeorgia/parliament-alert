import re
from django import forms
from django.utils.translation import ugettext as _

from parliament.apps.alerts.models import ParliamentAlert
from parliament.apps.categories.models import Category



class AlertForm(forms.ModelForm):
    regex_text = re.compile('[^a-zA-Z0-9\.,;:\ \'\"\?\-\/]')

    class Meta:
        model = ParliamentAlert
        fields = ('text_en','text_ka','categories','is_important')
        widgets = {
            'text_en': forms.Textarea(attrs={'cols':40, 'rows': 12}),
            'text_ka': forms.Textarea(attrs={'cols':40, 'rows': 12}),
        }


    def _clean_text (self, text):
        # returns callable-iterator, so we have to loop through 
        result = self.regex_text.finditer(text)
        indices = []
        for r in result:
            indices.append(str(r.start() + 1))

        if len(indices) == 0: # clean
            return text

        error = _('Illegal characters at:') + ' '
        error += ', '.join(indices)
        raise forms.ValidationError(error)


    def clean_text_en(self):
        return self._clean_text(self.cleaned_data['text_en'])
    def clean_text_ka(self):
        return self._clean_text(self.cleaned_data['text_ka'])



class SendAlertForm(forms.Form):
#    text = forms.CharField(widget=forms.TextInput(attrs={"readonly":True}))
#    categories = forms.ModelMultipleChoiceField(Category.objects.all(),
#        widget=forms.SelectMultiple(attrs={"readonly":True}))
#    is_important = forms.BooleanField(widget=forms.CheckboxInput(attrs={"readonly":True}))
#    language = forms.ChoiceField(ParliamentAlert.LANG_CHOICES,widget=forms.Select(attrs={"readonly":True}))
    null=forms.Field(label="",widget=forms.HiddenInput())
