from django.forms import ModelForm

from clever.models import Answer


class AnswerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Answer
        fields = ('text', )
