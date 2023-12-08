from django import forms


# Choices=[
#     ('0','sadness'),
#     ('1','anger'),
#     ('2','love'),
#     ('3','surprise'),
#     ('4','fear'),
#     ('5','joy'),
# ]
Choices=[
    ('0','select dataset'),
    ('1','dataset-1'),
    ('2','dataset-2'),
]
qChoices=[
    ('0','select query'),
    ('1','I feel blessed to know this family'),
    ('2','I want take a chance to label up'),
    ('3','I feel is he generous'),
    ('4','I feel transcendant and splendid'),
    ('5','I assumed it would feel casual'),
    ('6','I watched the news at the tv'),
    ('7','I am feeling stressed and more than a bit anxious'),
    ('8','I feel overwhelmed how about you'),
    ('9','I was feeling whether it be mad sad disappointed or peaceful'),
    ('10','I feel blessed beyond blessed to share my life with you each week')
]



class PredictForm(forms.Form):
    dataset=forms.ChoiceField(choices=Choices)
    query= forms.ChoiceField(choices=qChoices)
    


# class AddDataForm(forms.Form):
#     emotion = forms.ChoiceField(choices=Choices)
#     type = forms.CharField(label_suffix=' ',label="Write Emtion-Text",widget=forms.Textarea(attrs= {'cols': 50, 'rows': 5}))


