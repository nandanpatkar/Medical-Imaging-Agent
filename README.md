# Medical-Imaging-Agent

# 🏥 Medical Imaging Diagnosis Agent

A Streamlit-based application that uses AI to analyze medical images and provide detailed professional analysis.


## 🌟 Features

- Support for multiple medical imaging formats (DICOM, TIFF, JPG, PNG)
- AI-powered analysis of medical images using Google's Gemini model
- Structured reporting with key findings, diagnostic assessment, and patient-friendly explanations
- Integration with DuckDuckGo search for providing research context and medical literature references
- User-friendly interface with clear visualization of uploaded images

## 📋 Analysis Structure

The AI agent provides comprehensive reports including:

1. **Image Type & Region**
   - Imaging modality identification
   - Anatomical region analysis
   - Image quality assessment

2. **Key Findings**
   - Systematic observations
   - Abnormality detection with precise descriptions
   - Severity ratings

3. **Diagnostic Assessment**
   - Primary diagnosis with confidence level
   - Differential diagnoses
   - Evidence-based analysis

4. **Patient-Friendly Explanation**
   - Simple, clear language
   - Visual analogies
   - Common concerns addressed

5. **Research Context**
   - Recent medical literature
   - Standard treatment protocols
   - Relevant medical references

## ⚠️ Disclaimer

This tool is for **educational and informational purposes only**. All analyses should be reviewed by qualified healthcare professionals. Do not make medical decisions based solely on this analysis.

## 🛠️ Requirements

```
streamlit==1.40.2
phidata==2.7.3
Pillow==10.0.0
duckduckgo-search
google-generativeai==0.8.3
pydicom==2.4.3
numpy>=1.24.3
```

## 🔧 Installation

1. Clone this repository
   ```bash
   git clone https://github.com/username/medical-imaging-diagnosis.git
   cd medical-imaging-diagnosis
   ```

2. Create a virtual environment (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

1. Get your Google API key from [Google AI Studio](https://aistudio.google.com/apikey)

2. Run the Streamlit app
   ```bash
   streamlit run app.py
   ```

3. Open your web browser and go to `http://localhost:8501`

4. Enter your Google API key in the sidebar

5. Upload a medical image and click "Analyze Image"

## 📦 File Processing Capabilities

- **DICOM files**: Full support for radiological DICOM format
- **TIFF files**: Support for multi-layer TIFF medical images
- **Standard formats**: Support for JPG, JPEG, PNG

## 👨‍💻 Key Components

- `process_dicom()`: Handles DICOM file processing
- `process_tiff()`: Specialized TIFF file handling
- `process_uploaded_file()`: Determines file type and routes processing
- `medical_agent`: AI agent configured with Gemini model and DuckDuckGo search tool

## 🧠 AI Integration

This application uses Google's Gemini AI model through the Phi framework to analyze medical images. The agent is configured with:

- `Gemini`: Google's generative AI model for image analysis
- `DuckDuckGo`: Search tool for providing research context


