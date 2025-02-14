from fastapi import FastAPI, File, UploadFile
import tempfile
import re
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.chat_models import ChatOpenAI  # Updated
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings  # Updated
from langchain_community.vectorstores import FAISS  # Updated
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

app = FastAPI()

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = "your-api-key"

@app.post("/extract")
async def extract_paper(file: UploadFile = File(...)):
    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file.file.read())
        temp_path = temp_file.name

    # Load and process PDF
    loader = PyPDFLoader(temp_path)
    pages = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(pages)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(texts, embeddings)

    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-4"),
        retriever=vectorstore.as_retriever()
    )

    # Extract key insights
    insights = {
        "Algorithm Used": qa_chain.run("What algorithm is proposed in the paper?"),
        "Dataset Used": qa_chain.run("What dataset is used in the research?"),
        "Evaluation Metrics": qa_chain.run("What evaluation metrics are used?"),
        "Results Summary": qa_chain.run("Summarize the key results of the paper.")
    }

    # Generate Code
    code_prompt = PromptTemplate(
        input_variables=["algorithm", "dataset"],
        template="Generate a Python implementation for the algorithm '{algorithm}' using the dataset '{dataset}'."
    )
    code_chain = LLMChain(llm=ChatOpenAI(model_name="gpt-4"), prompt=code_prompt)
    generated_code = code_chain.run({
        "algorithm": insights["Algorithm Used"],
        "dataset": insights["Dataset Used"]
    })

    # Extract required libraries from the code
    def extract_libraries(code):
        pattern = r'^\s*(?:import|from)\s+([\w\d_.]+)'
        matches = re.findall(pattern, code, re.MULTILINE)
        return sorted(set(matches))

    required_libraries = extract_libraries(generated_code)

    # Generate requirements.txt
    requirements_txt = "\n".join(required_libraries)

    # Generate code explanation
    explanation_prompt = PromptTemplate(
        input_variables=["code"],
        template="Explain how the following Python code works in detail:\n{code}"
    )
    explanation_chain = LLMChain(llm=ChatOpenAI(model_name="gpt-4"), prompt=explanation_prompt)
    code_explanation = explanation_chain.run(generated_code)

    return {
        "insights": insights,
        "code": generated_code,
        "libraries": required_libraries,
        "requirements": requirements_txt,
        "explanation": code_explanation
    }

# Ensure that the API runs when executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
