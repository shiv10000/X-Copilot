import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
import logging

# Configure environment first
os.environ["TOKENIZERS_PARALLELISM"] = "false"

app = Flask(__name__, template_folder='templates', static_folder='static')

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class RagSystem:
    def __init__(self):
        self.query_engine = None
        self.rag_enabled = True  # Add RAG state flag
        self.initialize_pipeline()

    def toggle_rag(self):
        """Toggle RAG functionality on/off"""
        self.rag_enabled = not self.rag_enabled
        logger.info(f"RAG {'enabled' if self.rag_enabled else 'disabled'}")

    def initialize_pipeline(self):
        """Initialize RAG pipeline with error handling"""
        try:
            logger.info("Initializing RAG pipeline...")
            
            self.embedding_model = HuggingFaceEmbedding(
                model_name="BAAI/bge-small-en-v1.5"
            )
            
            self.language_model = Ollama(
                model="deepseek-r1:1.5b",
                request_timeout=600,
                temperature=0.3
            )

            documents = SimpleDirectoryReader("docs").load_data()
            if not documents:
                raise ValueError("No documents found in 'docs' directory!")

            self.index = VectorStoreIndex.from_documents(
                documents,
                embed_model=self.embedding_model,
                show_progress=True
            )
            
            self.query_engine = self.index.as_query_engine(
                llm=self.language_model,
                similarity_top_k=3
            )
            logger.info("RAG pipeline initialized successfully!")

        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            raise

rag_system = RagSystem()

@app.route('/toggle_rag', methods=['POST'])
def toggle_rag():
    try:
        rag_system.toggle_rag()
        return jsonify({
            "status": "success",
            "rag_enabled": rag_system.rag_enabled
        })
    except Exception as e:
        logger.error(f"RAG toggle error: {str(e)}")
        return jsonify({"status": "error"})

@app.route('/')
def home():
    """Serve the main interface"""
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def handle_query():
    try:
        query = request.form['query']
        rag_enabled = request.form.get('rag_enabled', 'true') == 'true'
        logger.info(f"Processing query ({'RAG' if rag_enabled else 'LLM'}): {query}")

        if rag_enabled:
            response = rag_system.query_engine.query(query)
        else:
            # Direct LLM call without RAG
            response = rag_system.language_model.complete(query)
            
        return jsonify({
            "response": str(response),
            "status": "success"
        })
    
    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        return jsonify({
            "response": f"Error: {str(e)}",
            "status": "error"
        })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=False)
