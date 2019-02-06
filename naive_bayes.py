import csv
import random
from math import log
import decimal
spam_count=0
ham_count=0
gen_count=0

def split_dataset(dataset, splitRatio):
	trainSize = int(len(dataset) * splitRatio)
	trainSet = []
	copy = list(dataset)
	while len(trainSet) < trainSize:
		index = random.randrange(len(copy))
		trainSet.append(copy.pop(index))
	return [trainSet, copy]

def get_stat(dataset):
	global spam_count,ham_count
	gen_count=len(dataset)
	for key in dataset:
		if dataset[key][0]!=0:
			ham_count+=1
		if dataset[key][1]!=0:
			spam_count+=1

def get_data(filename):
	lines = list(csv.reader(open(filename, "r", encoding="latin-1")))[1:]
	splitRatio = 0.67
	train, test = split_dataset(lines, splitRatio)
	dataset={}
	for line in train:
		words_in_sms=line[1].split('\W')
		for word in words_in_sms:
			if word not in dataset:
				dataset[word]=[0,0]
			elif line[0]=='ham':
				dataset[word][0]+=1
			else:
				dataset[word][1]+=1
	return dataset,test

def make_prediction(train_data,test_data):
	win=0
	for line in test:
		spam=0
		ham=0
		words_in_sms=line[1].split('\W')
		for word in words_in_sms:
			if word in train_data:
				spam+=log((1+train_data[word][1])/(gen_count+spam_count))
				ham+=log((1+train_data[word][0])/(gen_count+ham_count))
			else:
				spam+=log(1/(gen_count+spam_count))
				ham+=log(1/(gen_count+ham_count))
		if (spam<ham and line[0]=='spam') or (spam>ham and line[0]=='ham'):
			win+=1
	return round(win/len(test),2)


if __name__=='__main__':
	train,test=get_data('spam.csv')
	get_stat(train)
	print('{}%'.format(make_prediction(train,test)*100))

