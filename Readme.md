# 📄 Paper2Code: Research Paper Implementer 🚀

**Paper2Code** converts research papers into working **Python implementations** using AI. It extracts key insights like **algorithm, dataset, evaluation metrics, and results** and generates code with setup instructions.

## **✨ Features**
- 📄 Upload a research paper (PDF)
- 📝 Extract key insights (Algorithm, Dataset, Metrics, Results)
- 🖥️ Auto-generate Python implementation
- 📦 Detect & list required libraries (`requirements.txt`)
- ⚙️ Provide setup & execution instructions
- 📖 Explain generated code

## **🛠️ Installation**
```bash
git clone https://github.com/dhawan98/Paper2Code.git
cd Paper2Code
python -m venv venv && source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY="your-api-key"  # Windows: set OPENAI_API_KEY=your-api-key

Usage
Start the backend (FastAPI):   
python api.py  # or uvicorn api:app --reload   
Start the frontend (Streamlit):   
streamlit run ui.py   
