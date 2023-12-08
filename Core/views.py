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



train1=pd.read_csv("Core/data/train1.txt",names=['text','emotion'],sep=';')
train2=pd.read_csv("Core/data/train2.txt",names=['text','emotion'],sep=';')
#mytrain=[]

index1 = train1[train1.duplicated() == True].index
train1.drop(index1, axis = 0, inplace = True)
train1.reset_index(inplace=True, drop = True)

index2 = train2[train2.duplicated() == True].index
train2.drop(index2, axis = 0, inplace = True)
train2.reset_index(inplace=True, drop = True)

def dataframe_difference(df1, df2, which=None):
    comparison_df = df1.merge(
        df2,
        indicator=True,
        how='outer'
    )
    if which is None:
        diff_df = comparison_df[comparison_df['_merge'] != 'both']
    else:
        diff_df = comparison_df[comparison_df['_merge'] == which]
    return diff_df


def Removing_numbers(text):
    text=''.join([i for i in text if not i.isdigit()])
    return text

def lower_case(text):
    text = text.split()
    text=[y.lower() for y in text]
    return " " .join(text)

def Removing_punctuations(text):
    ## Remove punctuations
    text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,،-./:;<=>؟?@[\]^_`{|}~"""), ' ', text)
    text = text.replace('؛',"", )
    
    ## remove extra whitespace
    text = re.sub('\s+', ' ', text)
    text =  " ".join(text.split())
    return text.strip()

def Removing_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)


def normalize_text(df):
    df.text=df.text.apply(lambda text : lower_case(text))
    df.text=df.text.apply(lambda text : Removing_numbers(text))
    df.text=df.text.apply(lambda text : Removing_punctuations(text))
    df.text=df.text.apply(lambda text : Removing_urls(text))
    return df

def normalized_sentence(sentence):
    sentence= lower_case(sentence)
    sentence= Removing_numbers(sentence)
    sentence= Removing_punctuations(sentence)
    sentence= Removing_urls(sentence)
    return sentence

train1=normalize_text(train1)
train2=normalize_text(train2)

# train model
X_train1 = train1['text'].values
y_train1 = train1['emotion'].values

X_train2 = train2['text'].values
y_train2 = train2['emotion'].values

size1 =[train1.emotion.value_counts().get('joy',0),
       train1.emotion.value_counts().get('sadness',0),
       train1.emotion.value_counts().get('anger',0),
       train1.emotion.value_counts().get('fear',0),
       train1.emotion.value_counts().get('love',0),
       train1.emotion.value_counts().get('surprise',0)
       ]

size2 =[train2.emotion.value_counts().get('joy',0),
       train2.emotion.value_counts().get('sadness',0),
       train2.emotion.value_counts().get('anger',0),
       train2.emotion.value_counts().get('fear',0),
       train2.emotion.value_counts().get('love',0),
       train2.emotion.value_counts().get('surprise',0)
       ]


def train_model(model,data,targets):
    text_clf=Pipeline([('vect',TfidfVectorizer()),('clf',model)])
    text_clf.fit(data,targets)
    return text_clf

global log_reg1
global log_reg2
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
            asked_query=dict(qChoices)[fm.cleaned_data['query']]
            if(fm.cleaned_data['dataset'] == '1'):
                global log_reg1
                predict_arr=log_reg1.predict([normalized_sentence(asked_query)])
                predict_proba_arr = log_reg1.predict_proba([normalized_sentence(asked_query)])
                pred=predict_arr[0]
                
                for emotion,probability in zip(log_reg1.classes_, predict_proba_arr[0]):
                    if(emotion=='joy'):
                        chances[0] = round(probability * 100)
                    elif(emotion=='sadness'):
                        chances[1] = round(probability * 100)
                    elif(emotion=='anger'):
                        chances[2] = round(probability * 100)
                    elif(emotion=='fear'):
                        chances[3] = round(probability * 100)
                    elif(emotion=='love'):
                        chances[4] = round(probability * 100)
                    elif(emotion=='surprise'):
                        chances[5] = round(probability * 100)
            else:
                global log_reg2
                predict_arr=predict_arr=log_reg2.predict([normalized_sentence(asked_query)])
                predict_proba_arr = log_reg2.predict_proba([normalized_sentence(asked_query)])
                pred=predict_arr[0]
                
                for emotion,probability in zip(log_reg2.classes_, predict_proba_arr[0]):
                    if(emotion=='joy'):
                        chances[0] = round(probability * 100)
                    elif(emotion=='sadness'):
                        chances[1] = round(probability * 100)
                    elif(emotion=='anger'):
                        chances[2] = round(probability * 100)
                    elif(emotion=='fear'):
                        chances[3] = round(probability * 100)
                    elif(emotion=='love'):
                        chances[4] = round(probability * 100)
                    elif(emotion=='surprise'):
                        chances[5] = round(probability * 100)
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
    global log_reg1
    log_reg1 = train_model(RandomForestClassifier(random_state = 0), X_train1, y_train1)
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
    global log_reg2
    log_reg2 = train_model(RandomForestClassifier(random_state = 0), X_train2, y_train2)
    disAble2=False
    return redirect('train')