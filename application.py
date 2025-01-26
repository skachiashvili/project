import os
import uuid
from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load your TensorFlow model
MODEL_PATH = 'path_to_your_model.h5'  # Replace with the path to your trained model
model = load_model(MODEL_PATH)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_unique_filename(filename):
    """
    Generate a unique filename to avoid overwriting files with the same name.
    """
    ext = filename.rsplit('.', 1)[1].lower()  # Get the file extension
    unique_name = f"{uuid.uuid4().hex}.{ext}"  # Generate a unique filename
    return unique_name

def process_image(filepath):
    """
    Process the uploaded image and make a prediction using the TensorFlow model.
    """
    # Load and preprocess the image
    img = image.load_img(filepath, target_size=(224, 224))  # Adjust target_size as needed
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize the image

    # Make a prediction
    prediction = model.predict(img_array)
    return prediction

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Generate a unique filename for the uploaded file
            unique_filename = generate_unique_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)

            # Process the uploaded image and get the prediction
            prediction = process_image(filepath)

            # Return the prediction result
            return f"File uploaded successfully. Prediction: {prediction}"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)