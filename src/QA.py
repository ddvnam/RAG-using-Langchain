from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from retriever import create_retriever
from load_llm import load_llm
from prepare_vector_db import load_db

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

def get_answer(chain, question):
    res = chain.invoke({'query': question})
    return res['result']

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

print(get_answer(chain, "lịch sử hình thành trường Đại học Công nghệ"))
