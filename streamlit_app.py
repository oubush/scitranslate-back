# from googletrans import Translator
import streamlit as st
import re
import time
import uploader
import base64

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


# Helper function to create a download link
def get_binary_file_downloader_html(bin_data, file_label, button_text):
    b64 = base64.b64encode(bin_data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{file_label}">{button_text}</a>'


st.title("SciTranslate Web Service")
st.markdown("---")

st.sidebar.title("Instructions")
st.sidebar.markdown("1. Upload a .docx file for translation.")
st.sidebar.markdown("OR")
st.sidebar.markdown("2. Enter Russian text for translation.")
st.sidebar.markdown("---")
st.sidebar.markdown("[GitHub Repo](https://github.com/Ekaterina-Sinkova/SciTranslate)")

if not st.session_state.get('ctr'):
    st.session_state['ctr'] = 0

def print_message():
    st.session_state['ctr'] += 1
    print(st.session_state['ctr'])

# File upload section
st.subheader("Translate from a .docx file")
# uploaded_file = st.file_uploader("Upload a .docx file for translation", on_change=print_message)
# object_uuid = uploader.put_file(uploaded_file)

with st.form("my-form", clear_on_submit=True):
    uploaded_file = st.file_uploader("FILE UPLOADER")
    submitted = st.form_submit_button("UPLOAD!")

if submitted and uploaded_file is not None:
    st.write("UPLOADED!")
    st.session_state['object_uuid'] = uploader.put_file(uploaded_file)
    print(st.session_state['object_uuid'])
        # do stuff with your uploaded file

if st.button("Translate"):
    with st.spinner("Translating..."):
        time.sleep(2)
        file_to_upload = uploader.get_file(st.session_state['object_uuid'])
        st.download_button('Download Translated File', file_to_upload, file_name=f'{st.session_state["object_uuid"][:5]}.docx')

# if uploaded_file:
#     if st.button("Translate"):
#         with st.spinner("Translating..."):
#             time.sleep(2)
#             file_to_upload = uploader.get_file('87a3dae3-6485-4ac6-8084-4019504136b4') # object_uuid)
#             st.download_button('Download Translated File 2', file_to_upload, file_name='output2.docx')
#         #     st.markdown(get_binary_file_downloader_html(file_to_upload, "output.docx",
        #                                                     "Download Translated File"), unsafe_allow_html=True)
        # # new_object_uuid = 

                
# # Text input section
# st.subheader("Translate Russian text")
# user_input_text = st.text_area("Enter Russian text for translation and press Ctrl + Enter")
# if user_input_text:
#     # Make a POST request to the FastAPI server to process the text
#     # data = {"text": user_input_text}
#     # response = requests.post(f"{url}/translate_text", headers=headers, data=json.dumps(data))
#     # if response.status_code == 200:
#     #     response.encoding = 'utf-8'
#     sentences = tokenize_text(user_input_text)
#     translated_sentences = []
#     translator = Translator()
#     for sentence in sentences:
#         result = translator.translate(sentence, src='ru', dest='en')
#         translated_sentences.append(result.text)

#     st.text_area("Translation", value=' '.join(translated_sentences))
