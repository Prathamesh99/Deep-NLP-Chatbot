#Importing libraries
import numpy as np
import tensorflow as tf
import re
import time

#--------DATA PREPROCESSING---------

#importing the dataset

lines = open('movie_lines.txt', encoding='utf-8', errors='ignore').read().split('\n')
conversations = open('movie_conversations.txt', encoding='utf-8', errors='ignore').read().split('\n')

#Mapping id and lines
id2line = {}
for line in lines:
	_line = line.split(' +++$+++ ')
	if len(_line) == 5:
		id2line[_line[0]] = _line[4]
		
#List of conversations
conversations_id = []
for conversation in conversations[:-1]:
	_convers = conversation.split(' +++$+++ ')[-1][1:-1].replace("'", "").replace(" ", "")
	conversations_id.append(_convers.split(','))
		
#Getting the questions and answers
questions = []	
answers = []
for conversation in conversations_id:
	for i in range(len(conversation)-1):
		questions.append(id2line[conversation[i]])
		answers.append(id2line[conversation[i+1]])
		
#cleaning text
def clean_text(text):
	text = text.lower()
	text = re.sub(r"i'm", "i am", text)		
	text = re.sub(r"he's", "he is", text)		
	text = re.sub(r"she's", "she is", text)
	text = re.sub(r"that's", "that is", text)
	text = re.sub(r"what's", "what is", text)	
	text = re.sub(r"where'is", "where is", text)
	text = re.sub(r"\'ll", "will", text)
	text = re.sub(r"\'ve", "have", text)	
	text = re.sub(r"\'re", "are", text)	
	text = re.sub(r"\'d", "would", text)
	text = re.sub(r"won't", "will not", text)
	text = re.sub(r"['!&%()\"#/@:;<>{}+=~|.?,*-]", "", text)	
	return(text)			        
		
#Cleaning questions
clean_questions = []
for question in questions:
	clean_questions.append(clean_text(question))

#Cleaning answers
clean_answers = []	
for answer in answers:
	clean_answers.append(clean_text(answer))
	

#Count for each word
word2count = {}
for question in clean_questions:
	for word in question.split():
		if word not in word2count:
			word2count[word] = 1
		else:
			word2count[word]+=1
for answer in clean_answers:
	for word in answer.split():
		if word not in word2count:
			word2count[word] = 1
		else:
			word2count[word]+=1
			
#Unique words
threshold = 20
questionswords2int = {}
word_number = 0
for word, count in word2count.items():
	if count >= threshold:
		questionswords2int[word] = word_number
		word_number += 1
answerswords2int = {}
word_number = 0
for word, count in word2count.items():
	if count >= threshold:
		answerswords2int[word] = word_number
		word_number += 1	

#Adding last tokens			
tokens = ['<PAD>','<EOS>','<OUT>','<SOS>']
for token in tokens:
	questionswords2int[token] = len(questionswords2int)+1
for token in tokens:
	answerswords2int[token] = len(answerswords2int)+1
	
#Creating the inverse dictionary of the answerswords2int dictionary
answersint2word = {w_i: w for w, w_i in answerswords2int.items()}
	
#Adding EOS
for i in range(len(clean_answers)):
	clean_answers[i]+='<EOS>'
	
#Translating all the questions and the answers to integers
questions_into_int = []
for question in clean_questions:
	ints = []
	for word in question.split():
		if word not in questionswords2int:
			ints.append(questionswords2int['<OUT>'])
		else:
			ints.append(questionswords2int[word])
	questions_into_int.append(ints)
	
answers_into_int = []
for answer in clean_answers:
	ints = []
	for word in answer.split():
		if word not in answerswords2int:
			ints.append(answerswords2int['<OUT>'])
		else:
			ints.append(answerswords2int[word])
	answers_into_int.append(ints)
		
#Sorting questions and answers
sorted_clean_questions = []
sorted_clean_answers = []
for length in range(1, 25+1):
	for i in enumerate(questions_into_int):
		if len(i[1]) == length:
			sorted_clean_questions.append(questions_into_int[i[0]])
			sorted_clean_answers.append(answers_into_int[i[0]])
	
	
	
	