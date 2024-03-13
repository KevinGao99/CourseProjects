#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Jayeol Chun
# Date: 9/22/20 9:09 PM
"""Logistic Regression Model

Feel free to change/restructure the the code below
"""
import torch.nn as nn
import torch
from torchtext.vocab import GloVe
from torch.nn import functional as F

class Net(nn.Module):
  """This is where you implement your neural network. """
  pass


class LR(nn.Module):
    def __init__(self, labels, num_length):
        super(LR, self).__init__()
        self.layer1 = nn.Linear(num_length * 3, len(labels), bias = True)
        self.reset_parameters()
    
    def reset_parameters(self):
        nn.init.normal_(self.layer1.weight, std = .01)
        nn.init.constant_(self.layer1.bias, 0)
    
    def forward(self, arg1, conn, arg2):
        x = torch.cat([arg1.float(), conn.float(), arg2.float()], 1)
        x = self.layer1(x)
        o = torch.sigmoid(x)
        return o
        
    
class LR_Dense(nn.Module):
    def __init__(self, labels, vocab_size: int, num_embedding: int = 512, num_hidden: int = 256):
        super(LR_Dense, self).__init__()
        self.embedding = nn.Embedding(vocab_size, num_embedding)
        self.layer1 = nn.Linear(num_embedding * 3, num_hidden, bias = True)
        self.layer2 = nn.Linear(num_hidden, num_hidden, bias =True)
        self.layer3 = nn.Linear(num_hidden, len(labels), bias = True)
        self.act = nn.ReLU()
        self.reset_parameters()
        
    def reset_parameters(self):
        nn.init.normal_(self.layer1.weight, std = .01)
        nn.init.constant_(self.layer1.bias, 0)
        nn.init.normal_(self.layer2.weight, std = .01)
        nn.init.constant_(self.layer2.bias, 0)
        nn.init.normal_(self.layer3.weight, std = .01)
        nn.init.constant_(self.layer3.bias, 0)
    
    def forward(self, arg1, conn, arg2):
        arg1 = self.embedding(arg1.long())
        arg1 = torch.sum(arg1, 1)
        conn = self.embedding(conn.long())
        conn = torch.sum(conn, 1)
        arg2 = self.embedding(arg2.long())
        arg2 = torch.sum(arg2, 1)
        
        x = torch.cat([arg1, conn, arg2], 1)
        x = self.layer1(x)
        x = self.act(x)
        x = self.layer2(x)
        x = self.act(x)
        o = self.layer3(x)
        return o
    
class LR_Glove(nn.Module):
    def __init__(self, labels, num_features, GloVe_vectors, num_hidden):
        super(LR_Glove, self).__init__()
        self.embed = nn.Embedding.from_pretrained(GloVe_vectors)
        self.layer1 = nn.Linear(num_features, num_hidden, bias = True)
        self.layer2 = nn.Linear(num_hidden, num_hidden, bias = True)
        self.layer3 = nn.Linear(num_hidden, len(labels), bias = True)
        self.act = nn.ReLU()
        self.reset_parameters()
    
    def reset_parameters(self):
        nn.init.normal_(self.layer1.weight, std = .01)
        nn.init.constant_(self.layer1.bias, 0)
        nn.init.normal_(self.layer2.weight, std = .01)
        nn.init.constant_(self.layer2.bias, 0)
        nn.init.normal_(self.layer3.weight, std = .01)
        nn.init.constant_(self.layer3.bias, 0)
        
    def forward(self, arg1, conn, arg2):
        arg1 = self.embed(arg1.long())
        arg1 = torch.sum(arg1, 1)
        conn = self.embed(conn.long())
        conn = torch.sum(conn, 1)
        arg2 = self.embed(arg2.long())
        arg2 = torch.sum(arg2, 1)
        
        x = torch.cat([arg1, conn, arg2], 1)
        x = self.layer1(x)
        x = self.act(x)
        x = self.layer2(x)
        x = self.act(x)
        o = self.layer3(x)
        return o

class LR_CNN(nn.Module):
    def __init__(self, labels, num_features, GloVe_vectors, kernel_size:int = 3, hidden_size:int = 180):
        super(LR_CNN, self).__init__()
        self.embedding = self.embed = nn.Embedding.from_pretrained(GloVe_vectors)
        self.conv = nn.Conv1d(num_features, hidden_size, kernel_size)
        self.linear = nn.Linear(hidden_size, len(labels), bias=True)
        self.reset_parameters()

    def reset_parameters(self):
        print("Reset parameters")
        nn.init.normal_(self.linear.weight, std=0.01)
        nn.init.constant_(self.linear.bias, 0)

    def forward(self, arg1, conn, arg2):
        arg1 = self.embed(arg1.long())
        arg1 = torch.transpose(arg1, 1, 2)
        conn = self.embed(conn.long())
        conn = torch.transpose(conn, 1, 2)
        arg2 = self.embed(arg2.long())
        arg2 = torch.transpose(arg2, 1, 2)
        x = torch.cat([arg1, conn, arg2],1)

        s1 = self.conv(x)
        conv = F.relu(s1)
        conv = F.max_pool1d(conv, conv.shape[-1])
        conv = torch.squeeze(conv, -1)

        logits = self.linear(conv)
        return logits
    
class combined_CNN(nn.Module):    
    def __init__(self, labels, num_features, GloVe_vectors, kernel_size: int = 3, hidden_size: int = 128):
        super(combined_CNN, self).__init__()
        self.embed = nn.Embedding.from_pretrained(GloVe_vectors)
        self.conv = nn.Conv1d(num_features, hidden_size, kernel_size)
        self.layer1 = nn.Linear(num_features, hidden_size, bias = True)
        self.layer2 = nn.Linear(hidden_size * 2, len(labels), bias = True)
        self.act = nn.ReLU()
        self.reset_parameters()
    
    def reset_parameters(self):
        nn.init.normal_(self.layer1.weight, std = .01)
        nn.init.constant_(self.layer1.bias, 0)
        nn.init.normal_(self.layer2.weight, std = .01)
        nn.init.constant_(self.layer2.bias, 0)
    
    def forward(self, arg1, conn, arg2):
        arg1 = self.embed(arg1.long())
        conn = self.embed(conn.long())
        arg2 = self.embed(arg2.long())
        arg1c = torch.transpose(arg1, 1, 2)
        connc = torch.transpose(conn, 1, 2)
        arg2c = torch.transpose(arg2, 1, 2)
        xc = torch.cat([arg1c, connc, arg2c], 1)
        arg1h = torch.sum(arg1, 1)
        connh = torch.sum(conn, 1)
        arg2h = torch.sum(arg2, 1)
        xh = torch.cat([arg1h, connh, arg2h], 1)
        
        
        xc = self.conv(xc)
        xc = F.relu(xc)
        xc = F.max_pool1d(xc, xc.shape[-1])
        xc = torch.squeeze(xc, -1)
        
        xh = self.layer1(xh)
        xh = self.act(xh)
        x = torch.cat([xc, xh], 0)
        o = self.layer2(x)
        return o

