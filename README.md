# 🚀 Streamlit OCR App Deployment Guide

## Quick Start

### Option 1: Deploy to Streamlit Community Cloud (Recommended)

1. **Upload to GitHub:**
   - Create a new repository on GitHub
   - Upload `streamlit_ocr_app.py` and `requirements.txt`
   - Commit and push your changes

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "Create app"
   - Select your repository and set main file path to `streamlit_ocr_app.py`
   - Click "Deploy"

### Option 2: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# For Tesseract OCR, you need to install Tesseract binary:
# Ubuntu/Debian: sudo apt-get install tesseract-ocr
# macOS: brew install tesseract
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki

# Run the app
streamlit run streamlit_ocr_app.py
```

### Option 3: Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY streamlit_ocr_app.py .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_ocr_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t streamlit-ocr .
docker run -p 8501:8501 streamlit-ocr
```

## Features Included

✅ **Multiple OCR Engines**: EasyOCR and Tesseract support
✅ **Multi-language Support**: 10+ languages available
✅ **File Upload**: Support for JPG, PNG, BMP, TIFF formats
✅ **Text Download**: Export extracted text as .txt file
✅ **Statistics**: Character and word count
✅ **Responsive UI**: Clean, user-friendly interface
✅ **Error Handling**: Graceful error management

## Customization Options

### Adding More OCR Engines
```python
# Add PaddleOCR support
import paddleocr

ocr_engine = st.sidebar.selectbox(
    "Choose OCR Engine",
    ["EasyOCR", "Tesseract", "PaddleOCR"]
)

if ocr_engine == "PaddleOCR":
    ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(image_np, cls=True)
    extracted_text = "\n".join([line[1][0] for line in result[0]])
```

### Adding Image Preprocessing
```python
# Add image enhancement options
enhance_image = st.sidebar.checkbox("Enhance Image Quality")

if enhance_image:
    # Convert to grayscale
    image = image.convert('L')
    # Apply other preprocessing techniques
```

## Troubleshooting

**Common Issues:**

1. **Tesseract not found**: Install Tesseract binary on your system
2. **Memory issues**: Reduce image size or use CPU-only mode
3. **Poor accuracy**: Try different OCR engines or image preprocessing
4. **Deployment fails**: Check all dependencies are in requirements.txt

## Next Steps

- Add support for PDF files
- Implement batch processing
- Add confidence scores
- Include text translation features
- Add support for handwritten text recognition
