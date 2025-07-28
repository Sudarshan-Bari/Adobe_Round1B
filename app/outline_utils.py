import fitz
def extract_outline(pdf_path):
    # identical to Round 1A
    # ... (use extract_outline from above)
    # return outline dict
    pass # REPLACE with your extract_outline implementation

def extract_sections(pdf_path, outline):
    # break doc into heading sections, return [{title, page, text}, ...]
    doc = fitz.open(pdf_path)
    sections = []
    last_pg = 0
    for i, h in enumerate(outline['outline']):
        page_num = h['page']-1
        title = h['text']
        # Grab text from heading to next heading or end-of-doc
        next_page = (
            outline['outline'][i+1]['page']-1
            if i+1 < len(outline['outline'])
            else len(doc)-1
        )
        txt = ""
        for p in range(page_num, next_page+1):
            txt += doc[p].get_text()
        sections.append({"title": title, "page": page_num+1, "text": txt.replace('\n',' ')})
    return sections
