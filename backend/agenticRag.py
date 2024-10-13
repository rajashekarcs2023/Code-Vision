

import os
import requests
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from pinecone import Pinecone
from openai import OpenAI

# Load environment variables
load_dotenv()

# Set up API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = "91cb1a4f-653b-49cb-a0f9-b4ee9853ce27"

if not OPENAI_API_KEY or not PINECONE_API_KEY:
    raise ValueError("Please set OPENAI_API_KEY and PINECONE_API_KEY in your .env file")

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Pinecone setup
pc = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index_name = "documentation"  # Replace with your actual index name
pinecone_index = pc.Index(pinecone_index_name)

# Set up LlamaIndex Settings
Settings.llm = LlamaOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002", api_key=OPENAI_API_KEY)
Settings.chunk_size = 512
Settings.chunk_overlap = 20

# Set up vector store
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

def load_documents():
    """Load documents from the 'data' folder under the main project root"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(project_root, 'data')
    
    if not os.path.exists(data_directory):
        raise FileNotFoundError(f"The 'data' directory does not exist at {data_directory}")
    
    documents = SimpleDirectoryReader(data_directory).load_data()
    print(f"Loaded {len(documents)} documents from {data_directory}")
    return documents

def create_index(documents):
    """Create index from documents"""
    return VectorStoreIndex.from_documents(
        documents,
        vector_store=vector_store
    )

def get_initial_analysis():
    """Make initial API call to get analysis"""
    url = "http://127.0.0.1:8001/analyze/quality/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"API call failed: {e}")
        return None

def query_rag_system(index, query):
    """Query the RAG system"""
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return str(response)

def generate_final_report(initial_query, rag_response):
    """Generate final report using OpenAI"""
    prompt = f"""Based on the following analysis results from the RAG system, generate a comprehensive and detailed markdown report. The report should follow a structured format, and include sections for **Executive Summary**, **Detailed Findings**, **Actionable Recommendations**, and **Future Improvements**. Please ensure that the markdown includes:
    * A **clear summary** of the overall code quality, performance, security, and refactoring recommendations.
    * **Detailed analysis results** for each identified issue or improvement area, including explanations for why these issues are important.
    * **Actionable recommendations** for developers to resolve these issues, organized by priority.
    * Provide **next steps** for maintaining or improving the codebase, including suggestions for automated tools, best practices, or architectural changes.
    * Use proper markdown formatting, such as **headers**, **bullet points**, **code blocks**, and **tables** where necessary.
    Here are the results from the analysis:
    Initial Query: {initial_query}
    RAG System Response: {rag_response}
    """

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",  # or whichever model you prefer
            messages=[
                {"role": "system", "content": "You are an expert code analyst and technical writer."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating report with OpenAI: {e}")
        return None

def main():
    # Load documents and create index
    print("Loading documents and creating index...")
    documents = load_documents()
    index = create_index(documents)
    print("Index created successfully.")

    # Step 1: Get initial analysis
    print("Getting initial analysis...")
    initial_analysis = get_initial_analysis()
    if not initial_analysis:
        print("Failed to get initial analysis. Exiting.")
        return

    # Step 2: Use initial analysis as query for RAG system
    print("Querying RAG system...")
    rag_response = query_rag_system(index, str(initial_analysis))
    print("RAG system queried successfully.")

    # Step 3: Generate final report
    print("Generating final report...")
    final_report = generate_final_report(str(initial_analysis), rag_response)
    if not final_report:
        print("Failed to generate final report. Exiting.")
        return

    # Save the final report to a file
    with open("final_report.md", "w") as f:
        f.write(final_report)

    print("Final report saved to 'final_report.md'")

if __name__ == "__main__":
    main()