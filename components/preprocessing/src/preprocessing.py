import argparse
import pandas as pd
import numpy as np
import string
import re
import nltk
from nltk.corpus import stopwords
from sklearn import preprocessing
from google.cloud import storage
punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ''' + string.punctuation

# Arabic stop words with nltk
stop_words = stopwords.words()

arabic_diacritics = re.compile("""
                             ّ    | # Shadda
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)

def preprocess(text):
    
    '''
    text is an arabic string input
    
    the preprocessed text is returned
    '''
    
    #remove punctuations
    translator = str.maketrans('', '', punctuations)
    text = text.translate(translator)
    
    # remove Tashkeel
    text = re.sub(arabic_diacritics, '', text)
    
    #remove longation
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)

    text = ' '.join(word for word in text.split() if word not in stop_words)

    return text

def avg_word(sentence):
    words = sentence.split()
    if len(words) == 0:
        return 0
    return (np.floor(sum(len(word) for word in words)/len(words)))
  
def processing(input):
    data = pd.read_excel(input)
    data.drop(columns=["ID"])
    label_encoder = preprocessing.LabelEncoder()
    data["Sentiment"]= label_encoder.fit_transform(data["Sentiment"])
    data['Feed'] = data["Feed"].apply(preprocess)
    data['word_count'] = data['Feed'].apply(lambda x: len(str(x).split(" ")))
    data['char_count'] = data['Feed'].str.len() ## this also includes spaces
    data['avg_char_per_word'] = data['Feed'].apply(lambda x: avg_word(x))
    stop = stopwords.words('arabic')
    data['stopwords'] = data['Feed'].apply(lambda x: len([x for x in x.split() if x in stop]))
    data = data.sort_values(by='word_count',ascending=[0])
    data.to_csv("data_processed.csv")
    storage_client = storage.Client()
    bucket = storage_client.bucket(config.gs_bucket_name)
    bucket.blob('processed/data_processed.csv').upload_from_filename('data_processed.csv', content_type='text/csv')
    print("Raw Data Processed Sucessfully")
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description= "Input your desired data to be passed")
    parser.add_argument('--DataPath', type = str,
    help = 'Enter the data you want to upload here')
    args = parser.parse_args()
    processing(args.DataPath)