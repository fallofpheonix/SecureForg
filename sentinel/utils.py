def build_context(files: dict):
    context = ""
    for name, code in files.items():
        context += f"<file path='{name}'>\n{code}\n</file>\n"
    return context
