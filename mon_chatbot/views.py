from django.contrib.auth.models import User
from django.shortcuts import render
import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import random
import json
from pathlib import Path
from .forms import *
from .models import *
from GlobalApp.models import *
#Chemin  de notre dossier

BASE_DIR = Path(__file__).resolve().parent


#zone de d'analyse de message envoyé 

stemmer = PorterStemmer()
def tokenize(sentence):
       return nltk.word_tokenize(sentence)

def stem(word):
       return stemmer.stem(word.lower())


def bag_of_words(tk_sentence,all_words):
        tk_sentence =[stem(w) for w in tk_sentence]
        bag = np.zeros(len(all_words),dtype=np.float32)
        for idx , w in enumerate(all_words):
            if w in tk_sentence:
                bag[idx]=1.0
        return bag


#words =["Organize" ,"orGanizes","orgaNizing"]
#stemmed_words =[stem(w) for w in words]
#print(stemmed_words)

#entence =["hello","how","are","you"]
#ords    =["hi","hello","I","you","bye","thank","cool"]
#ag =bag_of_words,(sentence, words)

#Algorithme de Neural Network


class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size) 
        self.l2 = nn.Linear(hidden_size, hidden_size) 
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        # no activation and no softmax at the end
        return out


# Training the model
my_json_file= BASE_DIR / 'intents.json.json'

with open(my_json_file,'r',encoding='utf-8') as f:
    intents =json.load(f)





    
all_words = []
tags = []
xy = []
# loop through each sentence in our intents patterns
for intent in intents['intents']:
    tag = intent['tag']
    # add to tag list
    tags.append(tag)
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = tokenize(pattern)
        # add to our words list
        all_words.extend(w)
        # add to xy pair
        xy.append((w, tag))

# stem and lower each word
ignore_words = ['?', '.', '!']
all_words = [stem(w) for w in all_words if w not in ignore_words]
# remove duplicates and sort
all_words = sorted(set(all_words))
tags = sorted(set(tags))

# create training data
X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    # X: bag of words for each pattern_sentence
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(X_train)
y_train = np.array(y_train)

# Hyper-parameters
num_epochs = 1000
batch_size = 8
learning_rate = 0.001
input_size = len(X_train[0])
hidden_size = 8
output_size = len(tags)
#print(input_size, output_size)


class ChatDataset(Dataset):

    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    # support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # we can call len(dataset) to return the size
    def __len__(self):
        return self.n_samples


dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset,
                          batch_size=batch_size,
                          shuffle=True,
                          num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size, hidden_size, output_size).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)

        # Forward pass
        outputs = model(words)
        # if y would be one-hot, we must apply
        # labels = torch.max(labels, 1)[1]
        loss = criterion(outputs, labels)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
#
#   if (epoch+1) % 100 == 0:
#       print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')
#
#
#print(f'final loss: {loss.item():.4f}')
#
data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_words": all_words,
    "tags": tags
}

FILE = BASE_DIR / "data.pth"
torch.save(data, FILE)

#print(f'training complete. file saved to {FILE}')

#Commencemant de fichier CHAT.PY

with open(my_json_file,'r',encoding='utf-8') as f:
    intents =json.load(f)

data = torch.load(FILE)
input_size  = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words   = data["all_words"]
tags        = data["tags"]
model_state = data["model_state"]
model = NeuralNet(input_size, hidden_size, output_size).to(device)

model.load_state_dict(model_state)
model.eval()

bot_name="Lora"
def Get_Reponse(msg):
   
    sentence = tokenize(msg)
    X = bag_of_words(sentence,all_words)
    X = X.reshape(1,X.shape[0])
    X = torch.from_numpy(X)
  
    output=model(X)
    
    _, predictive = torch.max(output,dim=1)
    tag = tags[predictive.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predictive.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return  random.choice(intent["responses"])
   
    return "I do not understand..."



#My_view

def display_chatbot(request,id):
    pats = Patient.objects.all()
    list = []
    for pat in pats :
        list.append(pat.user)
    if request.user in list :  
        form = chatbotForm()
        user = User.objects.get(id=id)
        lora = User.objects.get(username= 'Lora')
        pat = Patient.objects.get(user=user)
        pat_l = Patient.objects.get(user=lora)
        if isinstance(pat, Patient):
            if request.method == 'POST':
               form = chatbotForm(request.POST)
               if form.is_valid():
                   mon_message = form.cleaned_data['message']
                   my_msg = Temp_Message.objects.create(user = pat , message=mon_message, to =lora)
                   my_msg.save()
                   ans_msg = Temp_Message.objects.create(user = pat_l , message=Get_Reponse(mon_message), to = user)
                   ans_msg.save()
        else :
            return render(request,"403.html")             
        context = {
            'form' : form,
            'tmp_msg' : Temp_Message.objects.all().order_by('creation_time'),
            'pat_l' : pat_l
        }       

        return render(request, "chatbot.html",context)
    return render(request,"403.html")
