class RecursiveCharacterTextSplitter:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200, separators: list[str] | None = None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", " ", ""]

    def split_text(self, text: str) -> list[str]:
        if not text:
            return []
        chunks = self._split_text(text, self.separators)
        return self._merge_splits(chunks)

    def _split_text(self, text: str, separators: list[str]) -> list[str]:
        if not separators:
            return list(text)
        
        separator = separators[0]
        remaining_separators = separators[1:]
        
        splits = list(text) if separator == "" else text.split(separator)
            
        good_splits = []
        for s in splits:
            if not s:
                continue
            if len(s) < self.chunk_size or not remaining_separators:
                good_splits.append(s)
            else:
                good_splits.extend(self._split_text(s, remaining_separators))
        return good_splits

    def _merge_splits(self, splits: list[str]) -> list[str]:
        docs: list[str] = []
        current_doc: list[str] = []
        total = 0
        for d in splits:
            _len = len(d)
            if total + _len + (1 if current_doc else 0) > self.chunk_size:
                if current_doc:
                    doc = " ".join(current_doc)
                    if doc:
                        docs.append(doc)
                    while total > self.chunk_overlap or (
                        total + _len + (1 if current_doc else 0) > self.chunk_size and total > 0
                    ):
                        total -= len(current_doc[0]) + (1 if len(current_doc) > 1 else 0)
                        current_doc = current_doc[1:]
                current_doc.append(d)
                total += _len + (1 if len(current_doc) > 1 else 0)
            else:
                current_doc.append(d)
                total += _len + (1 if len(current_doc) > 1 else 0)
        if current_doc:
            doc = " ".join(current_doc)
            if doc:
                docs.append(doc)
        return docs

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)