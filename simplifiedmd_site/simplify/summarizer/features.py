from __future__ import division
import math
import nltk
from math import cos
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.metrics import jaccard_similarity_score

"""
    Helper Functions for computing features
"""
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def compute_term_freq(sent):
    term_freq = {}
    for word in sent.split():
        if word in term_freq:
            term_freq[word] += 1
        else:
            term_freq[word] = 1
    return term_freq

"""
    Functions to compute features
"""
def theme_count(sent, theme_words):
    if len(sent) == 0:
        return 0
    count = 0
    for word in sent.split():
        if word in theme_words:
            count += 1
    return count/len(sent)

def sent_pos(pos, text_len):
    if pos == 0 or pos == text_len-1:
        return 1
    else:
        threshold = 0.2 * text_len
        minbound = threshold * text_len
        maxbound = 2 * threshold * text_len
        value = cos(math.radians((pos+1-minbound) * ((1/maxbound)-minbound)))
        return value

def sent_len(sent):
    words = sent.split()
    if len(words) < 3:
        return 0
    else:
        return len(words)

def sent_paragraph_pos(pos, text_len):
    if pos == 0 or pos == text_len-1:
        return 1
    else:
        return 0

def count_proper(sent, pos_tags):
    count = 0
    for word in sent.split():
        tag = pos_tags.get(word)
        if tag == 'NNP' or tag == 'NNPS':
            count += 1
    return count

def count_numerals(sent):
    if len(sent.split()) == 0:
        return 0
    else:
	    count = 0
	    for word in sent.split():
		    if is_number(word):
			    count += 1		
	    return count/len(sent.split())

def compute_tfisf(sent, transformed_text):
    term_freq = compute_term_freq(sent)
    sum = 0
    for key, value in term_freq.iteritems():
        sent_freq = 0
        for sentence in transformed_text:
            wordlist = sentence.split()
            if key in wordlist and (sentence != sent):
                sent_freq += 1
        if sent_freq > 0:
            sum += term_freq[key] * (len(transformed_text)-1/sent_freq)
    if sum > 0:
        return math.log10(sum)/len(term_freq)
    else:
        return 0

def compute_centroid_sim(sent, centroid):
    centroid_freq = compute_term_freq(centroid)
    sent_freq = compute_term_freq(sent)
    numerator = 0
    if len(centroid_freq) > len(sent_freq):
        for key, value in sent_freq.iteritems():
            if key in centroid_freq:
                numerator += value * centroid_freq[key]
    else:
        for key, value in centroid_freq.iteritems():
            if key in sent_freq:
                numerator += value * sent_freq[key]

    if numerator == 0:
        return 0
                
    sqrt_centroid = 0
    for key, value in centroid_freq.iteritems():
		sqrt_centroid += value ** 2
    sqrt_centroid = math.sqrt(sqrt_centroid)
	
    sqrt_sent = 0
    for key, value in sent_freq.iteritems():
		sqrt_sent += value ** 2
    sqrt_sent = math.sqrt(sqrt_sent)
	
    if sqrt_centroid == 0 or sqrt_sent == 0:
		return 0
    else:
        return numerator/(sqrt_centroid * sqrt_sent)
        
def compute_jaccard(a, b):
    stemmer = PorterStemmer()
    
    a_words = set([stemmer.stem(word) for word in word_tokenize(a)])
    b_words = set([stemmer.stem(word) for word in word_tokenize(b)])
    
    return len(a_words & b_words) / len(a_words | b_words)

