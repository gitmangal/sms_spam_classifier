import streamlit as st
import pickle
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y.copy()
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y.copy()
    y.clear()
    for i in text:
        y.append(ps.stem(i))
    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('mnb_model.pkl','rb'))

st.title("SMS Spam Classifier")

input_tst = st.text_area("Enter the SMS")
if st.button('Predict'):
        # preprocess
        transformed_sms= transform_text(input_tst)
        #vectorize
        vector_input= tfidf.transform([transformed_sms])
        #predict
        result = model.predict(vector_input)[0]
        # display
        if result == 1:
            st.header("Spam")
        else:
            st.header("Not Spam")

