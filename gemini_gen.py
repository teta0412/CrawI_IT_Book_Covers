##pip install -q -U google-generativeai
import google.generativeai as genai
import os
import csv


API_KEY = 'YOUR_API_KEY'
genai.configure(api_key=API_KEY)

image_folder_path = 'images'

# List all image files in the directory
image_files = [f for f in os.listdir(image_folder_path) if f.endswith(('jpg', 'jpeg', 'png', 'JPG'))]

for image_file in image_files:
    image_path = os.path.join(image_folder_path, image_file)

output_txt_path = '/Users/anhducnguyen/PycharmProjects/CrawI_IT_Books/Res_IT_Book_datasets.txt'
# Upload the file and print a confirmation.
start_index = 0  # Thay đổi giá trị nếu muốn tiếp tục từ một vị trí cụ thể
# Nếu chưa có file 'results.txt', tạo file mới (chế độ 'a' tự động tạo file mới nếu chưa tồn tại)
if not os.path.exists(output_txt_path):
    open(output_txt_path, 'w').close()  # Tạo file rỗng nếu chưa tồn tại
# Lặp qua các file hình ảnh từ start_index
for index, image_file in enumerate(image_files[start_index:], start=start_index):
    image_path = os.path.join(image_folder_path, image_file)
    print(image_path)
    f = genai.upload_file(image_path)

    model = genai.GenerativeModel("gemini-1.5-flash")
    try :
        result = model.generate_content(
            [f, "\n\n", """
            Từ hình ảnh được cung cấp, hãy thực hiện các tác vụ sau:
    
            1. Trích xuất tên tác giả của cuốn sách.
            2. Trích xuất tiêu đề của cuốn sách.
            3. Trích xuất tên nhà xuất bản.
            
            Xuất kết quả theo định dạng:

            - Câu hỏi: Tên tác giả là gì? / Tiêu đề cuốn sách là gì? / Nhà xuất bản là ai?
            - Câu trả lời: <Nội dung trích xuất>
            Lưu ý:
    
            - Nếu không tìm thấy tên tác giả không trả về kết quả
            - Nếu không tìm thấy nhà xuất bản không trả về kết quả
    
            Trả kết quả theo dạng cột với các trường: 'Câu hỏi', 'Câu trả lời'.
            """
            ]
        )
        with open(output_txt_path, mode="a", encoding="utf-8") as output_file:
            output_file.write(image_path + ';' + result.text)

        # In ra màn hình để theo dõi
        print(f"Đã xử lý ảnh {index}: {image_path}")
        print(f"Kết quả:\n{result.text}")
        print("############################################################")
    except Exception:
        print("An exception occurred")
        continue;


input_file = "Res_IT_Book_datasets.txt"
questions_answers = []

# Read the input file and extract data while ignoring lines with "Câu hỏi", "Câu trả lời"
with open(input_file, 'r', encoding='utf-8') as file:
    for line in file:
        # Check if it's an image path line
        if line.startswith("Image Path:"):
            image_path = line.strip().replace("Image Path: ", "")
        # Check if the line contains the question-answer pair
        elif "|---|" not in line and "|" in line and "Câu hỏi" not in line and "Câu trả lời" not in line:
            parts = line.strip().split("|")
            if len(parts) >= 3:
                question = parts[1].strip()
                answer = parts[2].strip()
                questions_answers.append([image_path, question, answer])

# Write the cleaned data to a new CSV file
clean_output_file = "results_cleaned.csv"
with open(clean_output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['image_path', 'question', 'answer'])  # Write header
    writer.writerows(questions_answers)

clean_output_file
