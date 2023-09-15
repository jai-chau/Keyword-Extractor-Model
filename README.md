<h1>Earnings Transcript Analysis</h1>

<h2>This tool facilitates the analysis of earnings call transcripts by extracting key phrases (bigrams) and displaying them. Developed using Python and Streamlit, it sources transcript data from roic.ai and highlights the most mentioned phrases to identify the main discussion points of the call.</h2>

<h3>Features:</h3>
  1) Enter specific details like Ticker, Year, Quarter, Number of Phrases Wanted, and custom words that you'd want to remove from analysis.
  <br>
  2) Utilizes NLP techniques to process and analyze the transcript.
  <br>
  3) Displays a table of the most common phrases (bigrams) from the transcript.

<h3>How To Use:</h3>
  1) Enter the required details in the sidebar.
  <br>
  2) The app will display the top phrases from the earnings call transcript based on the input details.

<h3>Important Note:</h3>
The tool scrapes data from roic.ai. If there's any change in the website structure of roic.ai, this tool might require modifications to work correctly.

<h3>Future Improvements (as outlined in the code comments):</h3>
  1) Extend the functionality to extract sentences where specific phrases are mentioned and calculate the sentiment of those sentences.
  <br>
  2) Develop a mechanism to determine the rate of change of sentiment quarter-over-quarter for recurring phrases.

<h3>Dependencies:</h3>
  <br>
  1) pandas
  <br>
  2) nltk
  <br>
  3) re (standard library)
  <br>
  4) requests
  <br>
  5) BeautifulSoup4
  <br>
  6) streamlit
  <br>
  7) streamlit-tags
  <br>

Disclaimer:
<br>
This tool is intended for educational and informational purposes only. It scrapes data from a third-party website, and the accuracy, timeliness, or completeness of the data cannot be guaranteed.
