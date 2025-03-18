#Handling PDFs, chunking and storing doc embeddings is done in this file
import os
from PyPDF2 import PdfReader
from Embedding_wrapper import get_embedding
from doc_search import store_embedding

def read_pdf(file_path):                         #Reads and extracts text from a PDF file
    print(f"Trying to open file: {file_path}")
    text = ""
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + " "
    return text.strip()

def chunk_text(text, chunk_size=30):              #Splits text into word-based chunks.
    words = text.split()
    if not words:  # Handle empty text cases
        return []
    words = text.split()
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def process_pdf_and_store(file_path):            #Processes a single PDF file, generates embeddings, and stores them in Cosmos DB
    text = read_pdf(file_path)  
    if not text:
        print(f"No text found in {os.path.basename(file_path)}")
        return

    chunks = chunk_text(text)  
    pdf_name = os.path.splitext(os.path.basename(file_path))[0]

    for i, chunk in enumerate(chunks):
        chunk_id = f"{pdf_name}_chunk_{i+1}"
        embedding = get_embedding(chunk)
        store_embedding(chunk_id, chunk, embedding)  # Calling store_embedding from doc_search

    print(f"Processed {len(chunks)} chunks from {os.path.basename(file_path)}.")

def process_multiple_pdfs_separately(directory_path):     #Processes each PDF in a folder separately
    if not os.path.exists(directory_path):
        print("Error: Directory does not exist.")
        return

    pdf_files = [f for f in os.listdir(directory_path) if f.endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the directory.")
        return

    print(f"Found {len(pdf_files)} PDF(s). Processing each separately...")

    for pdf in pdf_files:
        file_path = os.path.join(directory_path, pdf)
        print(f"\n🔹 Processing {pdf}...")
        process_pdf_and_store(file_path)

    print("\nAll PDFs processed separately.")

# Test function 
if __name__ == "__main__":
    folder_path = r"C:\Users\sankalp.datta\OneDrive - Optimus Information Inc\Desktop\ChatBot\Test"
    process_multiple_pdfs_separately(folder_path)
    #file_path=r"C:\Users\sankalp.datta\OneDrive - Optimus Information Inc\Desktop\ChatBot\Test\WFH Approval Guidelines "
