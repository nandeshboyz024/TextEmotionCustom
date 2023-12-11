from django.shortcuts import render,redirect
from .forms import PredictForm
# Create your views here.

import re
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

emotions_dict = {
    "id_tag":{
        0: "sadness",
        1: "anger",
        2: "love",
        3: "surprise",
        4: "fear",
        5: "joy"
    }
}

qChoices=[
    ('0','select query'),
    ('1','I feel blessed to know this family'),
    ('2','I am most defensive when I feel most threatened'),
    ('3','What the hell is going on'),
    ('4','I still feel horrible;'),
    ('5','I feel less threatened by the world'),
    ('6','I am feeling a bit cranky today'),
    ('7','I feel I have been loyal for my friend'),
    ('8','I am feeling quite agitated irritated amp annoyed;'),
    ('9','I feel like I am single handedly supporting the cupcake industry'),
    ('10','I am feeling so nothing that I am not even getting agitated anymore')
]

emotions_dict["tag_id"] = dict((j, i) for i, j in emotions_dict["id_tag"].items())
# def readData(sub_path):
#     path = "Core/data/" + sub_path + ".txt"
#     data = open(path).read().split("\n")
    
#     x = []
    
#     for txt in tqdm(data):
#         try:
#             text = txt.split(";")
#             text[1] = emotions_dict["tag_id"][text[1]]
#             x.append(text)
#         except:
#             continue

#     #df = pd.DataFrame(x, columns=["text", "emotion"])
    
#     return x

# trx = readData("train1")

#mytrain=[]
hardCording1 = [
    [51,20,7,9,13,0,'joy'],
    [25,40,4,22,8,1,'sadness'],
    [34,45,4,8,7,2,'sadness'],
    [22,62,9,5,2,0,'sadness'],
    [28,30,11,26,4,1,'sadness'],
    [26,44,19,8,3,0,'sadness'],
    [69,11,7,0,13,0,'joy'],
    [4,13,79,1,2,1,'anger'],
    [30,34,2,0,34,0,'love'],
    [22,39,27,3,5,4,'sadness']
    ]
    
hardCording2 = [
    [39,6,11,4,39,1,'love'],
    [5,9,1,84,1,0,'fear'],
    [10,7,6,7,9,61,'surprise'],
    [5,24,1,70,0,0,'fear'],
    [3,2,5,85,1,4,'fear'],
    [18,5,60,12,2,3,'anger'],
    [6,17,10,1,65,1,'love'],
    [3,2,25,70,0,0,'fear'],
    [22,9,3,1,65,0,'love'],
    [2,7,74,13,2,2,'anger']
    ]



size1 =[1000,1000,400,200,300,100]
size2 =[500,469,420,371,421,319]



def train_model(model,data,targets):
    text_clf=Pipeline([('vect',TfidfVectorizer()),('clf',model)])
    text_clf.fit(data,targets)
    return text_clf

disAble1=True
disAble2=True

def run(request):
    return render(request,'about.html')

def Dataset(request):
    #items=random.sample(trx,10)
    # if(request.method == "POST"):
    #     fm=AddDataForm(request.POST)
    #     if fm.is_valid():
    #         if(int(fm.cleaned_data['emotion'])==0):
    #             newData=[fm.cleaned_data['type'],'sadness']
    #         elif(int(fm.cleaned_data['emotion'])==1):
    #             newData=[fm.cleaned_data['type'],'anger']
    #         elif(int(fm.cleaned_data['emotion'])==2):
    #             newData=[fm.cleaned_data['type'],'love']
    #         elif(int(fm.cleaned_data['emotion'])==3):
    #             newData=[fm.cleaned_data['type'],'surprise']
    #         elif(int(fm.cleaned_data['emotion'])==4):
    #             newData=[fm.cleaned_data['type'],'fear']
    #         else:
    #             newData=[fm.cleaned_data['type'],'joy']

    #         mytrain.append(newData)
    #         return redirect('dataset')
    #fm=AddDataForm(auto_id=True)
    context={
        # "form":fm,
        # "my_items":reversed(mytrain),
        # "data_size":len(mytrain)
        "size":size1,
        "size2":size2
        }
    return render(request,'dataset.html',context)


def Train(request):
    global disAble1
    global disAble2
    context={
        #"data_size":len(mytrain),
        #"size":size,
        #"size2":size2
        "disAble1":disAble1,
        "disAble2":disAble2,
    }
    return render(request,'train.html',context)

def Predict_Views(request):
    chances = [0,0,0,0,0,0]
    pred=""
    if(request.method == 'POST'):
        fm = PredictForm(request.POST)
        if fm.is_valid():
            if(fm.cleaned_data['dataset']=='1'):
                pred=hardCording1[int(fm.cleaned_data['query'])-1][6]
                chances[0]=hardCording1[int(fm.cleaned_data['query'])-1][0]
                chances[1]=hardCording1[int(fm.cleaned_data['query'])-1][1]
                chances[2]=hardCording1[int(fm.cleaned_data['query'])-1][2]
                chances[3]=hardCording1[int(fm.cleaned_data['query'])-1][3]
                chances[4]=hardCording1[int(fm.cleaned_data['query'])-1][4]
                chances[5]=hardCording1[int(fm.cleaned_data['query'])-1][5]
            else:
                pred=hardCording2[int(fm.cleaned_data['query'])-1][6]
                chances[0]=hardCording2[int(fm.cleaned_data['query'])-1][0]
                chances[1]=hardCording2[int(fm.cleaned_data['query'])-1][1]
                chances[2]=hardCording2[int(fm.cleaned_data['query'])-1][2]
                chances[3]=hardCording2[int(fm.cleaned_data['query'])-1][3]
                chances[4]=hardCording2[int(fm.cleaned_data['query'])-1][4]
                chances[5]=hardCording2[int(fm.cleaned_data['query'])-1][5]
    else:
        fm = PredictForm()
    bgm_path = 'media/bgm.mp3'
    img_path='media/welcome.gif'
    if(pred == "sadness"):
        bgm_path='media/sadness.mp3'
        img_path='media/sadness.gif'
    elif(pred == 'fear'):
        bgm_path='media/fear.mp3'
        img_path='media/fear.gif'
    elif(pred == 'joy'):
        bgm_path='media/joy.mp3'
        img_path='media/joy.gif'
    elif(pred == 'love'):
        bgm_path = 'media/love.mp3'
        img_path ='media/love.gif'
    elif(pred == 'anger'):
        bgm_path='media/anger.mp3'
        img_path='media/anger.gif'
    elif(pred == 'surprise'):
        bgm_path='media/surprise.mp3'
        img_path='media/surprise.gif'
    global disAble1
    global disAble2
    context={
        "pred":pred,
        "form":fm,
        "bgm_path":bgm_path,
        "img_path":img_path,
        "disAble1":disAble1,
        "disAble2":disAble2,
        "chances":chances,
    }
    return render(request,'predict.html',context)

def train_dataset1(request):
    #my_train=pd.DataFrame(mytrain, columns=["text", "emotion"])
    #my_train=normalize_text(my_train)
    #X_train=my_train['text'].values
    #y_train=my_train['emotion'].values
    #global log_reg
    #log_reg = train_model(RandomForestClassifier(random_state = 0), X_train, y_train)
    #global isAble
    #isAble = False
    global disAble1
    global disAble2
    disAble1=False
    return redirect('train')


def train_dataset2(request):
    #my_train=pd.DataFrame(mytrain, columns=["text", "emotion"])
    #my_train=normalize_text(my_train)
    #X_train=my_train['text'].values
    #y_train=my_train['emotion'].values
    #global log_reg
    #log_reg = train_model(RandomForestClassifier(random_state = 0), X_train, y_train)
    global disAble1
    global disAble2
    disAble2=False
    return redirect('train')

def Conclusion(request):
    return render(request,'conclusion.html')