from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import gradio as gr

from src.retriever import create_retriever
from src.load_llm import load_llm
from src.prepare_vector_db import load_db


def create_prompt(template):
    prompt = PromptTemplate(template=template, input_variables=["context","question"])
    return prompt


def create_chain(llm, prompt, db):
    retriever = create_retriever(db)
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={'prompt': prompt}
    )
    return chain

db = load_db('vector_db/')
llm = load_llm()

template = '''
<|im_start|>system
Bạn là trợ lý AI thông minh, chuyên hỗ trợ sinh viên của Đại học Công nghệ. Khi trả lời, hãy cung cấp thông tin chi tiết, chính xác và dễ hiểu, nhưng chỉ giới hạn trong những nội dung có liên quan đến trường Đại học Công nghệ. Hãy giữ câu trả lời ngắn gọn, không đi sâu vào các nội dung ngoài phạm vi của trường. Nếu câu hỏi nằm ngoài phạm vi thông tin của trường, lịch sự từ chối trả lời.

Khi trả lời, vui lòng thực hiện các bước sau:
1. Trích xuất các chi tiết quan trọng từ thông tin tham khảo dưới đây nếu có.
2. Từ những chi tiết quan trọng đó đối chiếu với câu hỏi đưa ra bởi sinh viên.
3. Trả lời câu hỏi một cách chính xác, chỉ tập trung vào nội dung có liên quan đến trường.
4. Dịch câu trả lời sang Tiếng Việt và đảm bảo rõ ràng, dễ hiểu cho sinh viên.

Thông tin tham khảo:
{context}
<|im_end|>
<|im_start|>user
Câu hỏi của sinh viên:
{question}
<|im_end|>
<|im_start|>assistant
Câu trả lời (liên quan đến Đại học Công nghệ):
'''

prompt = create_prompt(template)
chain = create_chain(llm, prompt, db)

def get_answer(question):
    return chain.invoke(question)["result"]

with gr.Blocks() as rag_interface:

    gr.Markdown("<h1>University FAQ Helper</h1><p>Ask a question, and I’ll retrieve relevant information to provide an answer!</p>")

    # Input for the user's question
    question_input = gr.Textbox(label="Nhập câu hỏi của bạn", placeholder="Type your question here...", lines=2)

    # Output for the assistant's response
    answer_output = gr.Textbox(label="Câu trả lời", placeholder="Answer will appear here...", lines=6, interactive=False)

    # Define the submit button and link it to `answer_question`
    submit_button = gr.Button("Submit")
    submit_button.click(fn=get_answer, inputs=question_input, outputs=answer_output)

# Launch the interface
rag_interface.launch(inbrowser=True, share=False)
