from sklearn.feature_extraction.text import TfidfVectorizer

def rank_sections(sections, persona, job_to_be_done, top_n=5):
    q = persona + ". " + job_to_be_done
    docs = [s["text"] for s in sections]
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([q] + docs)
    query_vec = X[0]
    doc_vecs = X[1:]
    scores = (query_vec * doc_vecs.T).toarray()[0]
    # Rank by score
    ranked = []
    s_idxs = sorted(range(len(scores)), key=lambda i: -scores[i])[:top_n]
    for idx in s_idxs:
        ranked.append({
            "title": sections[idx]['title'],
            "page": sections[idx]['page'],
            "text": sections[idx]['text']
        })
    return ranked

