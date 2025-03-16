import os
import glob
import json
import csv
import torch
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain import hub
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

docs_arr=[]

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}

def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    docs_arr.append(docs_content)
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    chat = create_LLM()
    response = chat.invoke(messages)
    return {"answer": response.content}

def embed_model(model_name="intfloat/e5-large-v2", normalize=True, device=None):
    #intfloat/e5-large-v2
    #thenlper/gte-small
    if device is None:
        if torch.backends.mps.is_available():
            device = "mps"
            print("mps available:", torch.backends.mps.is_available())
        else:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print("CUDA available:", torch.cuda.is_available())
    torch.cuda.empty_cache()
    return HuggingFaceEmbeddings(
        model_name=model_name,
        multi_process=False,
        model_kwargs={"device": device},
        encode_kwargs={"normalize_embeddings": normalize},
    )

def create_LLM():
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.2-3B-Instruct",
        task="text-generation",
        max_new_tokens=512,
        do_sample=False,
        repetition_penalty=1.03,
    )
    chat = ChatHuggingFace(llm=llm, verbose=True)
    return chat

def json_to_string(doc_item: dict) -> str:
    text = []
    for key, value in doc_item.items():
        if isinstance(value, list):
            value = ', '.join(str(v) for v in value)
        if isinstance(value, str):
            value = value.strip()
        text.append(f"{key.capitalize()}: {value}")
    return "\n".join(text)

def load_documents(directory: str) -> List[Document]:
    docs = []
    file_paths = glob.glob(os.path.join(directory, '*.json'))
    for path in file_paths:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    content = json_to_string(item)
                    docs.append(Document(page_content=content, metadata=item))
    return docs

def answer_questions(question_file: str, answer_file: str):
    answers = {}
    with open(question_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for idx, row in enumerate(reader, start=1):
            if not row:
                continue
            question = row[0]
            print(f"Quesion {idx}: {question}")
            response = graph.invoke({"question": question})
            answers[str(idx)] = response["answer"]
    with open(answer_file, "w", encoding="utf-8") as f:
        json.dump(answers, f, indent=4)

if __name__ == "__main__":
    docs = load_documents("./docs")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = text_splitter.split_documents(docs)

    embedding_model = embed_model()
    faiss_path = "./faiss_index"

    if os.path.exists(faiss_path):
        vector_store = FAISS.load_local(faiss_path, embedding_model, allow_dangerous_deserialization=True)
    else:
        vector_store = FAISS.from_documents(all_splits, embedding_model)
        vector_store.save_local(faiss_path)
    prompt = hub.pull("rlm/rag-prompt")
    new_template = (
        "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If there is a highly related answer you can use that." 
        "If you cannot find a direct match or complete answer, but notice partial matches or somewhat relevant information in the context, provide that partial information as the answer"
        "If a question contains multiple parts to the answer then separate them with a semicolon. " 
        "Keep it accurate and don't answer in sentences. Whatever your answer is return only the answer don't give the justification." 
        "Sample questions and answers:"
        "Q: Who is Pittsburgh named after?"
        "A: William Pitt"
        "Q: What famous machine learning venue had its first conference in Pittsburgh in 1980?"
        "A: ICML"
        "Q: What musical artist is performing at PPG Arena on October 13?"
        "A: Billie Eilish"
        "Question: {question} Context: {context} Answer:"
    )
    prompt.messages[0].prompt.template = new_template

    print("New template:\n", prompt)

    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()

    input_csv = "questions.csv"  
    output_json = "answers.json"    
    answer_questions(input_csv, output_json)
