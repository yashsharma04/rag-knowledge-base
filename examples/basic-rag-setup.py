#!/usr/bin/env python3
"""
Basic RAG System Setup Example

This script demonstrates a simple RAG implementation using:
- ChromaDB for vector storage
- sentence-transformers for embeddings
- OpenAI for text generation

Requirements:
pip install chromadb sentence-transformers openai python-dotenv
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer
import openai
from dotenv import load_dotenv
from typing import List, Dict

# Load environment variables
load_dotenv()

class BasicRAGSystem:
    def __init__(self, collection_name: str = "rag_documents"):
        """Initialize the RAG system with embedding model and vector database."""
        self.collection_name = collection_name
        
        # Initialize embedding model
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB
        print("Initializing vector database...")
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize OpenAI (optional - for generation)
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
    def add_documents(self, documents: List[str], metadatas: List[Dict] = None):
        """Add documents to the vector database."""
        print(f"Adding {len(documents)} documents to the collection...")
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(documents).tolist()
        
        # Prepare metadata
        if metadatas is None:
            metadatas = [{"source": f"doc_{i}"} for i in range(len(documents))]
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=[f"doc_{i}" for i in range(len(documents))]
        )
        
        print(f"Successfully added {len(documents)} documents!")
    
    def search(self, query: str, n_results: int = 3) -> List[Dict]:
        """Search for relevant documents using semantic similarity."""
        print(f"Searching for: '{query}'")
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query]).tolist()
        
        # Search in collection
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'document': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })
        
        return formatted_results
    
    def generate_response(self, query: str, context_documents: List[str]) -> str:
        """Generate a response using OpenAI API with retrieved context."""
        if not openai.api_key:
            return "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        
        # Create augmented prompt
        context = "\n\n".join(context_documents)
        prompt = f"""Based on the following context, please answer the question.

Context:
{context}

Question: {query}

Answer:"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def rag_query(self, query: str, n_results: int = 3) -> Dict:
        """Complete RAG pipeline: retrieve relevant documents and generate response."""
        # Step 1: Retrieve relevant documents
        search_results = self.search(query, n_results)
        
        # Step 2: Extract document content
        context_documents = [result['document'] for result in search_results]
        
        # Step 3: Generate response
        response = self.generate_response(query, context_documents)
        
        return {
            'query': query,
            'retrieved_documents': search_results,
            'response': response
        }

def main():
    """Example usage of the BasicRAGSystem."""
    
    # Sample documents
    sample_documents = [
        "RAG (Retrieval-Augmented Generation) is a technique that combines information retrieval with text generation to enhance Large Language Models.",
        "Vector databases store document embeddings and enable fast semantic search through high-dimensional vector spaces.",
        "Chunking strategies are crucial for RAG systems, as they determine how documents are split into manageable pieces for processing.",
        "Embedding models convert text into numerical vectors that capture semantic meaning and enable similarity comparisons.",
        "The three main steps of RAG are: Retrieval (finding relevant documents), Augmentation (adding context to prompts), and Generation (creating responses)."
    ]
    
    # Initialize RAG system
    rag = BasicRAGSystem()
    
    # Add documents
    rag.add_documents(sample_documents)
    
    # Example queries
    queries = [
        "What is RAG and how does it work?",
        "What are the main components of a RAG system?",
        "How do vector databases work in RAG?"
    ]
    
    # Process queries
    for query in queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print(f"{'='*50}")
        
        result = rag.rag_query(query)
        
        print(f"\nRetrieved Documents:")
        for i, doc in enumerate(result['retrieved_documents'], 1):
            print(f"{i}. {doc['document'][:100]}... (distance: {doc['distance']:.3f})")
        
        print(f"\nGenerated Response:")
        print(result['response'])
        print(f"\n{'-'*50}")

if __name__ == "__main__":
    main()