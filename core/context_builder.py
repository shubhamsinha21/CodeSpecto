def build_context(file_index, query, max_chars=6000):
    keywords = query.lower().split()
    scored = []

    for f in file_index:
        score = sum(1 for k in keywords if k in f["content"].lower())
        if score > 0:
            scored.append((score, f))

    scored.sort(reverse=True, key=lambda x: x[0])

    context = ""
    for _, f in scored:
        snippet = f["content"][:2000]
        context += f"\n📄 {f['file_path']}:\n{snippet}\n"
        if len(context) >= max_chars:
            break

    return context
