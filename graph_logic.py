import os
import requests
import io
import time
from PIL import Image
from typing import TypedDict, List, Optional
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver 
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

class ContentState(TypedDict):
    raw_text: str
    video_script: str
    image_prompts: List[str] 
    twitter_thread: str

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

def query_hf(prompt):
    try:
        response = requests.post(HF_API_URL, headers=headers, json={"inputs": prompt}, timeout=60)
        if response.status_code == 503:
            time.sleep(15)
            return query_hf(prompt)
        return response.content if response.status_code == 200 else None
    except:
        return None

def scriptwriter_node(state: ContentState):
    res = llm.invoke(f"Write a viral 30s video script for: {state['raw_text']}")
    return {"video_script": res.content}

def prompt_designer_node(state: ContentState):
    res = llm.invoke(f"Describe 4 cinematic scenes for a storyboard. Max 15 words each, separated by |: {state['video_script']}")
    descriptions = res.content.split("|")
    local_paths = []
    for i, desc in enumerate(descriptions[:4]):
        img_bytes = query_hf(f"{desc.strip()}, cinematic, high resolution, dark aesthetic")
        if img_bytes:
            path = f"scene_{i}.png"
            Image.open(io.BytesIO(img_bytes)).save(path)
            local_paths.append(path)
    return {"image_prompts": local_paths}

def social_node(state: ContentState):
    res = llm.invoke(f"Create a viral Twitter thread for: {state['raw_text'][:500]}")
    return {"twitter_thread": res.content}

# --- Graph Assembly (No Video) ---
builder = StateGraph(ContentState)
builder.add_node("writer", scriptwriter_node)
builder.add_node("designer", prompt_designer_node)
builder.add_node("social", social_node)

builder.add_edge(START, "writer")
builder.add_edge("writer", "designer")
builder.add_edge("designer", "social")
builder.add_edge("social", END)

memory = MemorySaver()
factory_graph = builder.compile(checkpointer=memory)