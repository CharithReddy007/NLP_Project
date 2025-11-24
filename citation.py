# backend/citation.py
from sentence_transformers import SentenceTransformer, util
import nltk
nltk.download('punkt', quiet=True)
# FIX: Added 'punkt_tab' download to resolve LookupError
nltk.download('punkt_tab', quiet=True) 
from nltk.tokenize import sent_tokenize

embedder = SentenceTransformer("all-MiniLM-L6-v2")


def generate_citations(summary, original_text):
    """
    For each summary sentence → find the most similar source sentence.
    """

    summary_sents = sent_tokenize(summary)
    source_sents = sent_tokenize(original_text)

    # Encode sentences
    src_emb = embedder.encode(source_sents, convert_to_tensor=True)
    sum_emb = embedder.encode(summary_sents, convert_to_tensor=True)

    citations = []
    for i, emb in enumerate(sum_emb):
        hits = util.semantic_search(emb.unsqueeze(0), src_emb, top_k=1)[0]
        best = hits[0]

        citations.append({
            "summary_sentence": summary_sents[i],
            "source_sentence": source_sents[best['corpus_id']],
            "similarity_score": float(best['score'])
        })

    return citations