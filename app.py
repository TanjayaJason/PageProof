import streamlit as st
from pageproof.core import extract, answer

st.set_page_config(page_title='PageProof', page_icon='📑', layout='wide')
st.title('PageProof')
st.caption('Ask a question. Read the evidence. Follow the page.')
with st.sidebar:
    st.header('Your reading desk')
    st.write('Text PDFs · up to 5 files · 20 MB per file · 300 pages each')
    ai = st.toggle('Use configured LLM', value=False)
    st.caption('When enabled, the question and selected passages leave this computer.')
    if st.button('Clear document session'):
        for key in list(st.session_state):
            del st.session_state[key]
        st.session_state['upload_key'] = str(__import__('uuid').uuid4())
        st.rerun()
    st.caption('Documents are held in session memory; nothing is written to disk by this app.')
files = st.file_uploader('Add your PDFs', type=['pdf'], accept_multiple_files=True,
                         key=st.session_state.get('upload_key', 'initial'))
with st.form('question'):
    question = st.text_input('What would you like to find?', max_chars=1500,
                             placeholder='Apa syarat untuk mengajukan beasiswa?')
    submitted = st.form_submit_button('Find evidence', type='primary')
if submitted:
    try:
        with st.spinner('Reading and matching passages…'):
            chunks = extract([(f.name, f.getvalue()) for f in files])
            result = answer(chunks, question, ai)
        if result['mode'] == 'abstained':
            st.warning('Insufficient evidence to answer. Try a more specific question.')
        elif result['mode'] == 'retrieval':
            st.info('Local search results. These are matching passages, not a generated answer.')
        for claim in result['claims']:
            st.write(claim['text'])
            st.caption(f"{claim['file']} · page {claim['page']}")
            st.text(claim['quote'])
        st.subheader('Source passages')
        for item in result['evidence']:
            with st.expander(f"{item['file']} · page {item['page']}"):
                st.text(item['text'])
        st.download_button('Download result as JSON', __import__('json').dumps(result, indent=2),
                           'pageproof-result.json', 'application/json')
    except Exception as exc:
        st.error(str(exc) if isinstance(exc, (ValueError, OSError)) else 'Unable to read PDF or generate an answer.')
