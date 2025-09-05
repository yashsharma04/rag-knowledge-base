"""
Configuration file for RAG system examples.

This file contains configuration settings and constants used across
the RAG implementation examples.
"""

import os
from typing import Dict, Any

# Environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
WEAVIATE_URL = os.getenv('WEAVIATE_URL')

# Embedding model configurations
EMBEDDING_MODELS = {
    'all-MiniLM-L6-v2': {
        'name': 'all-MiniLM-L6-v2',
        'dimension': 384,
        'max_tokens': 256,
        'description': 'Compact and effective for most use cases'
    },
    'all-mpnet-base-v2': {
        'name': 'all-mpnet-base-v2',
        'dimension': 768,
        'max_tokens': 384,
        'description': 'Higher quality but larger model'
    },
    'text-embedding-ada-002': {
        'name': 'text-embedding-ada-002',
        'dimension': 1536,
        'max_tokens': 8191,
        'description': 'OpenAI\'s embedding model'
    }
}

# Vector database configurations
VECTOR_DB_CONFIGS = {
    'chromadb': {
        'type': 'chromadb',
        'persist_directory': './chroma_db',
        'collection_name': 'rag_documents',
        'distance_metric': 'cosine'
    },
    'pinecone': {
        'type': 'pinecone',
        'index_name': 'rag-index',
        'dimension': 384,
        'metric': 'cosine'
    },
    'weaviate': {
        'type': 'weaviate',
        'url': 'http://localhost:8080',
        'class_name': 'Document'
    }
}

# Chunking configurations
CHUNKING_CONFIGS = {
    'legal_documents': {
        'chunk_size': 1000,
        'chunk_overlap': 200,
        'method': 'paragraph',
        'description': 'For legal documents with structured paragraphs'
    },
    'technical_docs': {
        'chunk_size': 500,
        'chunk_overlap': 100,
        'method': 'section',
        'description': 'For technical documentation'
    },
    'conversations': {
        'chunk_size': 300,
        'chunk_overlap': 150,
        'method': 'sentence',
        'description': 'For conversational data'
    },
    'code_docs': {
        'chunk_size': 400,
        'chunk_overlap': 100,
        'method': 'function',
        'description': 'For code documentation'
    }
}

# LLM configurations
LLM_CONFIGS = {
    'gpt-3.5-turbo': {
        'model': 'gpt-3.5-turbo',
        'max_tokens': 1000,
        'temperature': 0.7,
        'cost_per_1k_tokens': 0.002
    },
    'gpt-4': {
        'model': 'gpt-4',
        'max_tokens': 2000,
        'temperature': 0.7,
        'cost_per_1k_tokens': 0.03
    },
    'claude-3-sonnet': {
        'model': 'claude-3-sonnet-20240229',
        'max_tokens': 2000,
        'temperature': 0.7,
        'cost_per_1k_tokens': 0.015
    }
}

# Retrieval configurations
RETRIEVAL_CONFIGS = {
    'conservative': {
        'similarity_threshold': 0.8,
        'top_k': 3,
        'description': 'High precision, lower recall'
    },
    'balanced': {
        'similarity_threshold': 0.7,
        'top_k': 5,
        'description': 'Balanced precision and recall'
    },
    'aggressive': {
        'similarity_threshold': 0.6,
        'top_k': 10,
        'description': 'Higher recall, lower precision'
    }
}

# Performance monitoring configurations
MONITORING_CONFIG = {
    'enable_logging': True,
    'log_level': 'INFO',
    'metrics_collection': True,
    'performance_tracking': True
}

# Security configurations
SECURITY_CONFIG = {
    'enable_encryption': True,
    'access_control': True,
    'audit_logging': True,
    'data_retention_days': 365
}

def get_config(config_type: str, config_name: str = None) -> Dict[str, Any]:
    """
    Get configuration for a specific type and name.
    
    Args:
        config_type: Type of configuration (e.g., 'embedding_models', 'chunking_configs')
        config_name: Specific configuration name (optional)
    
    Returns:
        Configuration dictionary
    """
    config_map = {
        'embedding_models': EMBEDDING_MODELS,
        'vector_db_configs': VECTOR_DB_CONFIGS,
        'chunking_configs': CHUNKING_CONFIGS,
        'llm_configs': LLM_CONFIGS,
        'retrieval_configs': RETRIEVAL_CONFIGS,
        'monitoring_config': MONITORING_CONFIG,
        'security_config': SECURITY_CONFIG
    }
    
    if config_type not in config_map:
        raise ValueError(f"Unknown config type: {config_type}")
    
    configs = config_map[config_type]
    
    if config_name is None:
        return configs
    
    if config_name not in configs:
        raise ValueError(f"Unknown config name: {config_name} for type: {config_type}")
    
    return configs[config_name]

def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate a configuration dictionary.
    
    Args:
        config: Configuration dictionary to validate
    
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['type', 'name']
    
    for field in required_fields:
        if field not in config:
            print(f"Missing required field: {field}")
            return False
    
    return True

# Example usage
if __name__ == "__main__":
    # Get embedding model config
    embedding_config = get_config('embedding_models', 'all-MiniLM-L6-v2')
    print("Embedding Model Config:", embedding_config)
    
    # Get chunking config
    chunking_config = get_config('chunking_configs', 'technical_docs')
    print("Chunking Config:", chunking_config)
    
    # Get all retrieval configs
    all_retrieval_configs = get_config('retrieval_configs')
    print("All Retrieval Configs:", all_retrieval_configs)