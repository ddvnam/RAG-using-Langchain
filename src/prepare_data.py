from posixpath import split
import os
import json
import re
import requests
from bs4 import BeautifulSoup
from langchain.document_loaders import WebBaseLoader, RecursiveUrlLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_child_links(url): 
    try:
        response = requests.get(url, verify=False)  
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
        unique_links = list(set(links))
        
        return unique_links
    except requests.exceptions.SSLError as e:
        print(f"SSL Error: {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return []

def save_links_to_file(url, filename):
    links = get_child_links(url)
    with open(filename, 'w') as file:
        for link in links:
            file.write(link + '\n')

save_links_to_file('http://tuyensinh.uet.vnu.edu.vn', 'web_links.txt')

# Hàm trích xuất và làm sạch nội dung từ HTML
def extract_and_clean(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.get_text()
    cleaned_content = re.sub(r'[^a-zA-Z0-9,.\s]', '', content)  # Loại bỏ ký tự đặc biệt
    cleaned_content = re.sub(r'\s+', ' ', cleaned_content).strip()
    return cleaned_content

# Hàm crawl dữ liệu web trực tiếp với WebBaseLoader và chỉ lấy các thẻ nội dung
def crawl_data_web(url_data):
    session = requests.Session()
    session.verify = False
    # Thiết lập User-Agent để giả lập trình duyệt
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    })

    # Tải nội dung HTML từ URL
    response = session.get(url_data)
    response.raise_for_status()  # Kiểm tra nếu có lỗi trong quá trình tải trang

    # Sử dụng BeautifulSoup để lấy nội dung từ các thẻ cụ thể
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trích xuất nội dung từ các thẻ mong muốn (ví dụ: <p>, <h1>, <h2>)
    content = []
    for tag in soup.find_all(['p', 'h1', 'h2', 'h3']):
        content.append(tag.get_text(strip=True))

    full_content = ' '.join(content)

    # Chuyển nội dung thành định dạng tài liệu cho LangChain
    # using Document class from langchain.schema
    docs = [Document(page_content=full_content, metadata={"source": url_data})]

    # Sử dụng TextSplitter để chia nhỏ tài liệu
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(docs)

    print('Số lượng đoạn văn bản:', len(docs))
    return docs

def save_data(documents, filename, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, filename)

    # Chuyển đổi documents thành định dạng có thể serialize
    data_to_save = [{'page_content': doc.page_content, 'metadata': doc.metadata} for doc in documents]

    # Lưu vào file JSON với encoding UTF-8
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data_to_save, file, ensure_ascii=False, indent=4)
    print(f'Data saved to {file_path}')

def get_links_from_file(file_path):
    with open(file_path, 'r') as file:
        links = file.read().splitlines()
    return links

links_web = 'data/web_links.txt'
links_web = get_links_from_file(links_web)
data_web = []

for link in links_web:
  data_web.extend(crawl_data_web(link))
  
save_data(data_web, 'data_web.json', 'data')
