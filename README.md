![image_alt](https://github.com/user-attachments/assets/3fb48404-3472-4ee5-aff7-349f3d41f83f)

# Retrieval-Augmented Generation (RAG) Project

Dự án này được thiết kế để cung cấp cho sinh viên mới một cách thuận tiện để truy cập thông tin trường đại học thông qua lời nhắc bằng ngôn ngữ tự nhiên, tận dụng Công nghệ thế hệ tăng cường truy xuất (RAG) với LangChain.

## Project Overview

Hệ thống RAG cho phép người dùng đặt câu hỏi bằng ngôn ngữ tự nhiên và lấy câu trả lời có liên quan bằng cách kết hợp mô hình ngôn ngữ với kho lưu trữ vector để truy xuất. Trong trường hợp này, LangChain được sử dụng để quản lý các quy trình truy xuất và tạo, trong khi mô hình LLaMA được triển khai làm mô hình ngôn ngữ.

## Features

- **Prompt-based Information Retrieval**: Người dùng có thể nhập câu hỏi, và hệ thống sẽ truy xuất và trình bày thông tin liên quan.
- **Vector Store Integration**: Sử dụng FAISS để lưu trữ và truy vấn biểu diễn vectơ của nội dung.
- **Web Interface**: Một giao diện web dựa trên Gradio cho phép người dùng tương tác với hệ thống một cách dễ dàng.
