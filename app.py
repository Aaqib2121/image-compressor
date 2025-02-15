from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
COMPRESSED_FOLDER = "compressed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

def compress_and_save(image_path, output_path, target_size_kb=300, min_quality=10, max_quality=85):
    with Image.open(image_path) as img:
        img = img.convert("RGB")  # Ensure compatibility
        
        quality = max_quality  # Start with high quality
        img.save(output_path, "JPEG", quality=quality, optimize=True)
        
        while os.path.getsize(output_path) > target_size_kb * 1024 and quality > min_quality:
            quality -= 5  # Reduce quality step by step
            img.save(output_path, "JPEG", quality=quality, optimize=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress_image():
    if 'image' not in request.files:
        return redirect(url_for('index'))

    file = request.files['image']
    if file.filename == '':
        return redirect(url_for('index'))

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    compressed_file_path = os.path.join(COMPRESSED_FOLDER, "compressed_" + file.filename)
    
    # Compress with adaptive quality adjustment
    compress_and_save(file_path, compressed_file_path, target_size_kb=300)

    return send_file(compressed_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# python3 app.py //Run Command