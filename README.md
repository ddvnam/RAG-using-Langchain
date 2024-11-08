![University FAQ Assistant](https://github.com/user-attachments/assets/3fb48404-3472-4ee5-aff7-349f3d41f83f)

# RAG for Q&A on University Information

## Project Overview

Dự án này cung cấp trợ lý FAQ của trường đại học được hỗ trợ bởi hệ thống Retrieval-Augmented Generation (RAG). Mục tiêu là cho phép người dùng, đặc biệt là sinh viên mới, nhanh chóng tìm thấy câu trả lời cho các câu hỏi về quy định và chính sách của trường đại học bằng cách nhập truy vấn bằng ngôn ngữ tự nhiên. Hệ thống RAG sẽ truy xuất thông tin có liên quan và tạo ra phản hồi mạch lạc, cải thiện khả năng truy cập và trải nghiệm của người dùng.

## How to Run the Project

### Requirements
- Python 3.x
- Gradio
- FAISS
- Underthesea (Xử lý văn bản)
- ChatGroq model API (Llama-3.1-70b-versatile hoặc model khác)
- LangChain

### Setup Steps
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <project_directory>
2. Cài đặt các thư viện cần thiết từ file requirements.txt:
   ```bash
   pip instal -r requirements.txt
3. Chạy file main.py:
   ```bash
   python main.py
4. Truy cập giao diện web và bắt đầu đặt câu hỏi về Thông tin về Trường Đại học Công Nghệ.

