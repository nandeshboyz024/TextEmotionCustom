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
    ('2','I am most defensive when I feel most threatened'),
    ('3','What the hell is going on'),
    ('4','I still feel horrible'),
    ('5','I feel less threatened by the world'),
    ('6','I am feeling a bit cranky today'),
    ('7','I feel I have been loyal for my friend'),
    ('8','I am feeling quite agitated irritated and annoyed'),
    ('9','I feel like I am single handedly supporting the cupcake industry'),
    ('10','I am feeling so nothing that I am not even getting agitated anymore')
]



class PredictForm(forms.Form):
    dataset=forms.ChoiceField(choices=Choices)
    query= forms.ChoiceField(choices=qChoices)
    


# class AddDataForm(forms.Form):
#     emotion = forms.ChoiceField(choices=Choices)
#     type = forms.CharField(label_suffix=' ',label="Write Emtion-Text",widget=forms.Textarea(attrs= {'cols': 50, 'rows': 5}))


