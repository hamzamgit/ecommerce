from django import forms
from products.models import RatingAndReviewModel


class RatingModelForm(forms.ModelForm):
    CHOICES = [(1, ''),
               (2, ''),
               (3, ''),
               (4, ''),
               (5, '')]

    def __init__(self, **kwargs):
        super(RatingModelForm, self).__init__(**kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.fields['rating_rating'] = forms.ChoiceField(choices=self.CHOICES, widget=forms.RadioSelect(
            attrs={'required': True}))

    class Meta:
        model = RatingAndReviewModel
        fields = ['rating_title', 'rating_review', 'rating_rating', 'rating_user', 'rating_time']
        exclude = ['rating_time']
