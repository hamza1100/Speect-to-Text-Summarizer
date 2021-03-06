# Importing the Libraries

import re
import heapq
import bs4 as bs
import urllib.request
import matplotlib.pyplot as plt

from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk import word_tokenize, sent_tokenize, download

download('stopwords')
download('punkt')

# Opening File for writing

text_file = open("Summary.txt", "w")

# Reading Data

text = open("sampleText.txt","r").read() # import text file extracted from audio

# Cleaning Data

text = re.sub(r'\[[0-9]*\]',' ',text)    
text = re.sub(r'\s+',' ',text)
clean_text = text.lower()
clean_text = re.sub(r'\W',' ',clean_text)
clean_text = re.sub(r'\d',' ',clean_text)
clean_text = re.sub(r'\s+',' ',clean_text)

stop_words = stopwords.words('english')

tokenized_sentences = sent_tokenize(text)
tokenized_words = word_tokenize(clean_text)

# Generating Dictionary for plotting

word2count = {}

for word in tokenized_words:
    if word not in stop_words:
        if word not in word2count.keys():
            word2count[word]=1
        else:
            word2count[word]+=1


# Separating Words and it's count for plotting

count=list(word2count.values())
words=list(word2count.keys())

# Plotting Unprocessed Data with frequency

plt.figure(1, figsize=(20, 20))
fdist = FreqDist(tokenized_words)
fdist.plot()

# Weighted Histogram

for key in word2count.keys():
    word2count[key]=word2count[key]/max(word2count.values())
  
# Calculate the score

sent2score = {}
for sentence in tokenized_sentences:
    for word in word_tokenize(sentence.lower()):
        if word in word2count.keys():
            if len(sentence.split(' '))<30:
                if sentence not in sent2score.keys():
                     sent2score[sentence]=word2count[word]
                else:
                    sent2score[sentence]+=word2count[word]

# Top n Sentences

best_sentences = heapq.nlargest(5,sent2score,key=sent2score.get)                    

for sentences in best_sentences:
    text_file.write('• ' + sentences + '\n')

text_file.close()


# Plotting bar plot after processing
plt.figure(1, figsize=(20, 20))
plt.bar(words, count, width=0.7)
plt.xticks(rotation=90)
plt.title('Words Count Plot')
plt.show()
