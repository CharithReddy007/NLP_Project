from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

MODEL_PATH = r"D:/NIKHIL/MAHINDRA UNIVERSITY/sem 5/NLP/PROJECT/models/bart-large-cnn"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)

print("Loading model...")
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH, local_files_only=True)

def summarize_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=300,
        min_length=40,
        num_beams=8,
        length_penalty=1.5,
        early_stopping=True
    )
    
    final_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    partial_summaries = []   # or something meaningful
    
    return final_summary, partial_summaries


if __name__ == "__main__":
    sample = "Artificial intelligence is transforming the world..."
    print(summarize_text(sample))
