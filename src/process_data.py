import re
import json

def flatten_content(data):
    # Trích xuất page_content và metadata
    page_content = data.get("page_content", "")
    metadata = data.get("metadata", {})

    # Làm phẳng nội dung
    flat_content = re.sub(r'\n+', '\n', page_content).strip()  # Loại bỏ dòng trống
    flat_content = re.sub(r'\s+', ' ', flat_content)  # Thay thế nhiều khoảng trắng bằng một khoảng trắng

    # Lấy thông tin tiêu đề và nguồn từ metadata
    title = metadata.get("title", "No Title")
    source = metadata.get("source", "No Source")

    # Kết hợp chỉ giữ lại content, source
    result = f"Content:{flat_content}|Source:{source}"
    return result

def word_segmentation(text):
    from underthesea import word_tokenize
    return word_tokenize(text, format="text")

processed_data = []
with open('data/data_web.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    for item in data:
        processed_data.append(word_segmentation(flatten_content(item)))

# Lưu vào file
with open('data/processed_data.json', 'w', encoding='utf-8') as file:
    json.dump(processed_data, file, ensure_ascii=False, indent=4)
