import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

class RAGKnowledgeBase:
    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.knowledge_chunks = [
            "Web Application Security Engineering requires OWASP Top 10, Burp Suite, and secure coding practices.",
            "GRC (Governance, Risk, and Compliance) focuses on risk assessments, ISO 27001, and compliance frameworks.",
            "Data Science roadmaps require Python, Pandas, Machine Learning, and SQL proficiency."
        ]
        self.embeddings = self.encoder.encode(self.knowledge_chunks)
        self.dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(np.array(self.embeddings).astype('float32'))

    def query(self, query_text, k=2):
        query_vector = self.encoder.encode([query_text])
        distances, indices = self.index.search(np.array(query_vector).astype('float32'), k)
        results = [self.knowledge_chunks[i] for i in indices[0]]
        return results
