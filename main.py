'''
Things to add:
1) Get sentences in which the phrases are in and calculate sentiment of those sentences
2) Rate of change of sentiment quarter over quarter for phrases that repeat
'''

#Importing the necessary packages
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import nltk
from collections import Counter
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.corpus import stopwords
import streamlit as st
from streamlit_tags import st_tags_sidebar 

nltk.download('punkt')
nltk.download('stopwords')

#Streamlit app title
st.set_page_config(layout="wide")
st.title("Earnings Transcript Analysis")

#Inputting the Ticker, Year, Quarter, Number of Phrases Wanted, and Custom Words to be Removed from the sidebar
ticker = st.sidebar.text_input("Ticker", value='', max_chars=5)
year = st.sidebar.number_input("Year", min_value=1, max_value=2030, value=2023)
quarter = st.sidebar.number_input("Quarter", min_value=1, max_value=4, value=2)
topNum = st.sidebar.number_input("Number of Outputs Wanted", min_value=1, max_value=100, value=10)
customRemovedWords = st_tags_sidebar(label='Custom Words to be removed', text='Press enter to add more', value=["quarter", "billion", "year", "million", "basis points"])

def insertColon(text):
    return re.sub(r'([a-zA-Z]+)([A-Z][a-z]+)', r'\1: \2', text)

#Getting the earnings call transcript from roic.ai
#IMPORTANT[THIS ENTIRE CODE WILL STOP WORKING IF ROIC.AI CHANGES THEIR WEBSITE STRUCTURE]
def earningsTranscript(ticker):
    eTranscript = []
    url = f"https://roic.ai/transcripts/{ticker}:US/{year}/{quarter}"
    agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers= agent)

    html = response.text
    soup = BeautifulSoup(html,'lxml')

    transcript_divs = soup.find_all('div', class_='relative max-w-xl rounded-xl rounded-tl-none bg-muted px-4 py-2 leading-normal shadow')

    for transcript in transcript_divs:
        eTranscript.append(insertColon(transcript.get_text(strip=True)))

    return eTranscript

#Cleaning the earnings call transcript text by removing the names of members in the company and any custom words/phrases specified by the user
def cleanedText(transcript, customRemovals=[]):
    # This regex matches names at the start of a string followed by a colon
    pattern = re.compile(r'^([a-zA-Z\s]+):')

    names = []
    # Extract names and lower them
    for item in transcript:
        match = pattern.match(item)
        if match:
            name = match.group(1).lower()
            names.append(name)

    # Ensure unique names
    uniqueNames = set(names)

    # Remove any instance of the name occurring in the list
    cleanedList = []
    for item in transcript:
        cleanedItem = item.lower()
        for name in uniqueNames:
            cleanedItem = cleanedItem.replace(name, "")
        for word in customRemovals:
            cleanedItem = cleanedItem.replace(word.lower(), "")
        cleanedList.append(cleanedItem.strip(": "))

    return cleanedList

#Extracting all the important bigrams and trigrams from the cleaned earnings call transcript
def extractKeywords(transcript_list, top_n=10):
    transcript = ' '.join(transcript_list)
    
    words = nltk.word_tokenize(transcript.lower())
    filteredWords = [word for word in words if word not in stopwords.words('english') and word.isalpha()]

    word_freq = Counter(filteredWords)
    bigramFinder = BigramCollocationFinder.from_words(filteredWords)

    # Get the frequencies of the bigrams
    bigrams_with_freq = {k: v for k, v in bigramFinder.ngram_fd.items()}

    # Sort the bigrams by frequency
    sorted_bigrams = sorted(bigrams_with_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Extract phrases and their frequencies
    phrases = [' '.join(phrase[0]) for phrase in sorted_bigrams]
    frequencies = [phrase[1] for phrase in sorted_bigrams]

    # Create a DataFrame
    df = pd.DataFrame({
        'Phrases': phrases,
        'Frequency': frequencies,
    })
        
    return df

# Usage example:
# df = extractKeywords(transcript_list)
# print(df)

# Example usage 
transcript = cleanedText(earningsTranscript(ticker), customRemovedWords)
topPhrases = extractKeywords(transcript, topNum)
#print("Top Keywords:", topKeywords)
#print("Top Phrases:", topPhrases)

#Outputing the Tables with data
if ticker:
    #Table for the Top Phrases of Specified Year and Quarter
    st.subheader(f"Top Phrases for {ticker} in {year} Quarter {quarter}:")
    st.table(topPhrases)
else:
    st.subheader("Enter a ticker")
