from __future__ import division

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, PunktSentenceTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.neural_network import BernoulliRBM

import numpy as np
import json
import operator
from features import *

example_text = "Alkaptonuria is a rare genetic metabolic disorder characterized by the accumulation of homogentisic acid in the body. Affected individuals lack enough functional levels of an enzyme required to breakdown homogentisic acid. Affected individuals may have dark urine or urine that turns black when exposed to air. However, this change may not occur for several hours after urination and often goes unnoticed. Aside from dark urine that is present from infancy, affected individuals generally do not develop symptoms (asymptomatic) during infancy or childhood and often remain unaware of their condition until adulthood. Affected individuals eventually develop ochronosis, which is the bluish-black discoloration of connective and other tissue within the body. Affected individuals may develop discoloration of the skin overlying cartilage within the body such as over part of the outer ear. In some cases, the whites of the eyes (sclera) may also become discolored. In adulthood, affected individuals also develop progressive arthritis of the spine and large joints. The HDG gene codes for the enzyme required for the breakdown of homogentisic acid. Mutations in HDG cause alkaptonuria. Adding more random sentences. Testing stuff yay! People over age of 50 get alkaptonuria."

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

sentences = sent_tokenize(example_text)
normalized_words_pos = {}
norm_word_freq = {}
transformed_text = []

for sent in sentences:
    # split words of sentencea
	sent_words = word_tokenize(sent)
	transformed_sent = []
	
	for tag in nltk.pos_tag(sent_words):
		# remove stop words
		if tag[0].lower() in stop_words:
			continue
        # stem word and increment count of word
		else:
			norm_word = stemmer.stem(tag[0])
            
			if norm_word[0].isalnum():

				if norm_word not in normalized_words_pos:
					normalized_words_pos[norm_word] = tag[1]

				transformed_sent.append(norm_word)

				if norm_word in norm_word_freq:
					norm_word_freq[norm_word] += 1
				else:
					norm_word_freq[norm_word] = 1
    
	transformed_text.append(" ".join(transformed_sent).strip())

# extract the popular words as our thematic words
norm_word_freq = sorted(norm_word_freq.iteritems(), key=operator.itemgetter(1), reverse=True)
theme_words = [x[0] for x in norm_word_freq[:10]]

# find the centroid sentence
tfisf_computations = {}
for sentence in transformed_text:
	score = compute_tfisf(sentence, transformed_text)
	tfisf_computations[sentence] = score
tfisf_scores = sorted(tfisf_computations.iteritems(), key=operator.itemgetter(1), reverse=True)

# create the sentence-feature matrix
sent_feat_mat = np.zeros(shape=(len(transformed_text), 8))
# fill in values for each feature for each sentence
for i in range(len(transformed_text)):
    sent_feat_mat[i] = [theme_count(transformed_text[i], theme_words), 
                        sent_pos(i, len(transformed_text)), 
                        sent_len(transformed_text[i]), 
                        sent_paragraph_pos(i, len(transformed_text)), 
                        count_proper(transformed_text[i], normalized_words_pos), 
                        count_numerals(transformed_text[i]), 
                        tfisf_computations[transformed_text[i]], 
                        compute_centroid_sim(transformed_text[i], tfisf_scores[0][0])]

# train a Restricted Boltzman Machine based on the sentence-feature matrix
model = BernoulliRBM(n_components=8, batch_size=4, n_iter=5)
model.fit(sent_feat_mat)

# enhance the original scores of the original sentence-feature matrix
sent_scores = []
for i in range(len(sentences)):
    sent_scores.append(
                (i, np.sum(np.dot(sent_feat_mat[i], model.components_) 
                    + model.intercept_visible_))
                )
                
sent_scores.sort(key = lambda tup : tup[1], reverse=True)

# extract sentence with the top score
top_sent = sentences[sent_scores[0][0]]
del sent_scores[0]

# parameter for number of sentences in summary
k = 3

# generate summary
summary = [top_sent]
for i in range(k):
    top_half_scores = sent_scores[:int(len(sent_scores)/2)]
    highest_jaccard = -1
    next_sent = None
    for score in top_half_scores:
        jaccard_score = compute_jaccard(top_sent, sentences[score[0]])
        if jaccard_score > highest_jaccard:
            highest_jaccard = jaccard_score
            next_sent = score
    summary.append(sentences[next_sent[0]])
    del sent_scores[next_sent[0]]
    
print " ".join(summary).strip()
