from googletrans import Translator
import streamlit as st
import re
import time

def tokenize_text(text: str) -> list:
    """Tokenizes input text into sentences using regex"""
    regex = r"(?<!гр)(?<!см)(?<!им)(?<!\sо)(?<!\sг)(?<!\sр)(?<!\.[А-Я])(?<!\.\s[А-Я])(\. +[А-Я])(?!\.)"
    r1 = re.split(regex, text)
    sents = [r1[0] + "."]
    for i in range(1, len(r1), 2):
        sents.append(r1[i][-1] + r1[i + 1] + ".")
    sents[-1] = sents[-1][0:-1]
    sents = [sent for sent in sents if re.search("[а-яА-Яa-zA-Z]", sent)]
    return sents

st.title("SciTranslate Web Service")
st.markdown("---")

st.sidebar.title("Instructions")
st.sidebar.markdown("1. Upload a .docx file for translation.")
st.sidebar.markdown("OR")
st.sidebar.markdown("2. Enter Russian text for translation.")
st.sidebar.markdown("---")
st.sidebar.markdown("[GitHub Repo](https://github.com/Ekaterina-Sinkova/SciTranslate)")

# # File upload section
st.subheader("Translate from a .docx file")
uploaded_file = st.file_uploader("Upload a .docx file for translation")
if uploaded_file:
    if st.button("Translate"):
        with st.spinner("Translating..."):
            time.sleep(2)
                
# Text input section
st.subheader("Translate Russian text")
user_input_text = st.text_area("Enter Russian text for translation and press Ctrl + Enter")
if user_input_text:
    # Make a POST request to the FastAPI server to process the text
    # data = {"text": user_input_text}
    # response = requests.post(f"{url}/translate_text", headers=headers, data=json.dumps(data))
    # if response.status_code == 200:
    #     response.encoding = 'utf-8'
    sentences = tokenize_text(user_input_text)
    translated_sentences = []
    translator = Translator()
    for sentence in sentences:
        result = translator.translate(sentence, src='ru', dest='en')
        translated_sentences.append(result.text)

    st.text_area("Translation", value=' '.join(translated_sentences))
