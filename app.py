# backend/app.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

# 1. Initialize FastAPI ONLY ONCE
app = FastAPI()

# 2. CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Correct Imports (ensure these are correctly pointed to your backend files)
from backend.summarizer import summarize_text
from backend.citation import generate_citations
from backend.rouge_eval import compute_rouge
from backend.utils import extract_pdf, extract_txt 


# 4. Corrected /summarize Endpoint Logic
@app.post("/summarize")
async def summarize(file: UploadFile = File(...)):
    # Use os.path.splitext for safer extension extraction
    ext = os.path.splitext(file.filename)[1].lower() 
    
    # Read file bytes once
    file_bytes = await file.read() 

    # Extract text based on file extension
    if ext == ".pdf":
        text = extract_pdf(file_bytes)
    elif ext == ".txt":
        text = extract_txt(file_bytes)
    else:
        # Raise a clear error for unsupported types
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file format: {ext}. Please upload PDF or TXT."
        )
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from file or file is empty.")

    # Run the processing pipeline
    final_summary, partial_summaries = summarize_text(text)
    citations = generate_citations(final_summary, text)
    
    # ROUGE requires a reference; use a slice of the text as a placeholder
    # Note: Using the first 1/5th of the text as a placeholder reference summary for testing.
    rouge_metrics = compute_rouge(final_summary, text[:len(text)//5]) 


    # 5. Return ALL data, including the necessary rouge_metrics
    return {
        "summary": final_summary,
        "chunk_summaries": partial_summaries,
        "citations": citations,
        "rouge_metrics": rouge_metrics 
    }

@app.post("/rouge")
async def rouge_eval(system_summary: str, reference_summary: str):
    return compute_rouge(system_summary, reference_summary)

@app.get("/")
def hi():
    return {"message": "Backend working!"}