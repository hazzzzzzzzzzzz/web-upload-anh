import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
app.secret_key = "super_secret_key" 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Đường dẫn đặc biệt để Flask có thể hiển thị được ảnh từ thư mục uploads lên web
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
                
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Upload ảnh thành công!')
            return redirect(url_for('upload_file'))
        else:
            flash('Định dạng file không hợp lệ! Chỉ nhận: png, jpg, jpeg, gif')
            return redirect(request.url)

    # Đoạn code quét toàn bộ ảnh trong thư mục uploads để gửi ra màn hình
    images = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        images = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]
        
    return render_template('index.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)