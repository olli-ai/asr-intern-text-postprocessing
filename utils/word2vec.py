import re
from collections import Counter

import gensim
import nltk
import numpy as np
import torch
from gensim.models import KeyedVectors
from torch.nn.utils.rnn import pad_sequence

from .token import idx2token, token, token2idx, token2vec


def word2vec(sentences, labels):
	'''
	sentences: list(string)
	labels   : list(string)
	'''
	# Count frequency of each word
	cnt = Counter()
	for snt in sentences:
	    for wd in nltk.word_tokenize(snt):
	        cnt.update([wd])

	# Create a map from word to frequency and reverse
	word2idx = {k:v for k,v in cnt.items()}
	idx2word = {v:k for k,v in cnt.items()}
	print('MAP FROM WORD TO FREQUENCY:')
	print(word2idx)
	print('\n','-'*50,'\n')
	print(idx2word)


	for i, snt in enumerate(sentences):
	    sentences[i] = [word2idx[w] for w in nltk.word_tokenize(snt)]
	labels = [[token2idx[lb] for lb in nltk.word_tokenize(lbs)] for lbs in labels]
	return sentences, labels, len(cnt.items())

def tkvec2lbsnt(lb_sentences):
	'''
	[[1,0,2,3],
	 [5,6,1,0]]

	----->

	[[]]
	'''
	a = torch.argmax(lb_sentences, dim = 2)
	return [' '.join([idx2token[lb.item()] for lb in snt]) for snt in a]

def word2vecVN(sentences,labels):
	model = 'baomoi.model.bin'
	word2vec_model = KeyedVectors.load_word2vec_format(model, binary=True)
	snts = []
	for snt in sentences:
		snt = snt.split()
		ws = []
		
		for word in snt:
			try:
				ws.append(torch.tensor(word2vec_model.get_vector(word).reshape((1,-1))))
			except:
				if model == 'wiki.vi.model.bin':
					# ws = torch.concat([ws, torch.ones((400,0))], dim=0)
					ws.append(torch.ones((400,0)))
				elif model == 'baomoi.model.bin':
					# ws = torch.concat([ws, torch.ones((400,0))], dim=0)
					ws.append(torch.ones((400,0)))

		snts.append(torch.concat(ws, dim = 0))
	snts = pad_sequence(snts,batch_first=True)
	labels = [torch.tensor([token2idx[lb] for lb in nltk.word_tokenize(lbs)]) for lbs in labels]
	labels = pad_sequence(labels,batch_first=True) 
	return snts, labels
