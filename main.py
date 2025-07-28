import os
import json
import fitz  # PyMuPDF
import time
from sentence_transformers import SentenceTransformer, util

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def load_metadata():
    meta_path = os.path.join(INPUT_DIR, "meta.json")
    with open(meta_path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_sections(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4].strip()
            if len(text.split()) >= 5:  # skip short labels
                sections.append({
                    "document": os.path.basename(pdf_path),
                    "page": page_num + 1,
                    "text": text
                })

    return sections

def rank_sections(sections, query, model, top_k=5):
    corpus = [s["text"] for s in sections]
    corpus_embeddings = model.encode(corpus, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)

    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=top_k)[0]

    extracted_sections = []
    sub_sections = []

    for rank, hit in enumerate(hits):
        idx = hit["corpus_id"]
        section = sections[idx]
        extracted_sections.append({
            "document": section["document"],
            "page": section["page"],
            "section_title": section["text"][:80] + "...",
            "importance_rank": rank + 1
        })
        sub_sections.append({
            "document": section["document"],
            "page": section["page"],
            "refined_text": section["text"]
        })

    return extracted_sections, sub_sections

def main():
    metadata = load_metadata()
    model = SentenceTransformer("/app/model")

    all_sections = []
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]

    for file in pdf_files:
        sections = extract_sections(os.path.join(INPUT_DIR, file))
        all_sections.extend(sections)

    query = metadata["persona"] + " " + metadata["job"]

    extracted_sections, sub_sections = rank_sections(all_sections, query, model)

    output = {
        "metadata": {
            "documents": pdf_files,
            "persona": metadata["persona"],
            "job": metadata["job"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "extracted_sections": extracted_sections,
        "sub_section_analysis": sub_sections
    }

    out_path = os.path.join(OUTPUT_DIR, "round1b_output.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
