import json
import os
import glob
from outline_utils import extract_outline, extract_sections
from rank_utils import rank_sections

INPUT_DIR = '/app/input'
OUTPUT_DIR = '/app/output'

def main():
    # Read persona/job and docs from a provided meta-input
    with open(os.path.join(INPUT_DIR, "meta.json"), encoding="utf-8") as f:
        meta = json.load(f)

    persona = meta["persona"]
    job = meta["job_to_be_done"]
    doc_files = meta["documents"]
    results = {
        "input_documents": doc_files,
        "persona": persona,
        "job_to_be_done": job,
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "sections": [],
        "subsections": []
    }
    # For each doc, extract (title, outline), sections & text per section
    for fname in doc_files:
        pdf_path = os.path.join(INPUT_DIR, fname)
        outline = extract_outline(pdf_path)
        sects = extract_sections(pdf_path, outline)
        # Rank section relevance
        ranked = rank_sections(sects, persona, job)
        for i, hit in enumerate(ranked):
            results["sections"].append({
                "document": fname,
                "page": hit["page"],
                "section_title": hit["title"],
                "importance_rank": i+1
            })
            # Sub-section analysis, e.g. summary (showing a snippet or summarized main points)
            results["subsections"].append({
                "document": fname,
                "page": hit["page"],
                "section_title": hit["title"],
                "refined_text": hit["text"]
            })
    # Output result
    out_name = "output.json"
    with open(os.path.join(OUTPUT_DIR, out_name), 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
