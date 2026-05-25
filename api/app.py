import os
from flask import Flask, render_template, request, redirect, url_for, flash
import vercel_blob

# Sửa lại dòng này để Vercel định vị chính xác thư mục templates
app = Flask(__name__, template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')))
app.secret_key = "super_secret_key"

# Vercel sẽ tự động đọc token lưu trữ khi bạn bấm nút Connect Storage lúc nãy

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Không tìm thấy file nào!')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('Bạn chưa chọn file nào cả!')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                # Đọc dữ liệu file ảnh
                file_bytes = file.read()
                # Tải thẳng lên kho Vercel Blob vĩnh viễn
                vercel_blob.put(file.filename, file_bytes, {"access": "public"})
                flash('Upload ảnh lên đám mây Vercel thành công!')
                return redirect(url_for('upload_file'))
            except Exception as e:
                flash(f'Lỗi khi upload: {str(e)}')
                return redirect(request.url)
        else:
            flash('Định dạng file không hợp lệ!')
            return redirect(request.url)

    # Lấy danh sách toàn bộ ảnh đã lưu trên Vercel Blob để hiện ra màn hình
    images = []
    try:
        blob_list = vercel_blob.list()
        for b in blob_list.get('blobs', []):
            images.append(b.get('url'))
    except Exception as e:
        print(f"Lỗi lấy ảnh: {e}")
        
    return render_template('index.html', images=images)

# Dòng này cực kỳ quan trọng để Vercel không bị lỗi Internal Server Error
app = app