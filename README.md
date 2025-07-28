📄 Adobe Challenge 1B – Persona-Based PDF Insight Generator
Developed by Gajula Lakshmi Naga Varshitha, Gajjarapu Padmaja

🧠 Problem Statement
Build a system that generates insights from PDFs tailored to a persona and a job role. It should:

Work fully offline

Be CPU-only

Fit under 200MB for code + model

Accept multiple PDFs + a meta.json file

Output ranked section insights as structured JSON

✅ Features
Persona-aware relevance ranking

Supports multiple PDFs in batch

Offline embeddings using sentence-transformers

Dockerized and stateless

Outputs structured .json to /output

📁 Folder Structure
graphql
Copy
Edit
adobe_round1b/
├── input/                  # Your PDF files + meta.json go here
├── output/                 # Output JSON files appear here
├── download_model.py       # One-time model downloader
├── inference.py            # Main script
├── utils.py                # Helpers for chunking, similarity, etc.
├── requirements.txt        # Dependencies
├── Dockerfile              # Docker image setup
└── README.md               # You're reading it :)
🐳 Docker Setup
Step 1: 🔧 Download the Model (One-Time Setup)
In your host machine (before Docker):

bash
Copy
Edit
python download_model.py
✅ This downloads sentence-transformers/all-MiniLM-L6-v2 to a model/ folder.

Step 2: 🛠️ Build the Docker Image
In the root project directory:

bash
Copy
Edit
docker build --platform linux/amd64 -t round1b:pdfinsight .
Step 3: 📥 Add Input Files
Put the following into the input/ folder:

One or more PDFs (.pdf)

A meta.json file like:

json
Copy
Edit
{
  "persona": "PhD Researcher in Computational Biology",
  "job": "Prepare a literature review on graph neural networks"
}
Step 4: 🚀 Run the Docker Container
PowerShell (recommended):
bash
Copy
Edit
docker run --rm `
  -v ${PWD}/input:/app/input `
  -v ${PWD}/output:/app/output `
  --network none `
  round1b:pdfinsight
CMD (Command Prompt):
cmd
Copy
Edit
docker run --rm ^
  -v %cd%/input:/app/input ^
  -v %cd%/output:/app/output ^
  --network none ^
  round1b:pdfinsight
🧾 Example Output (output/result.json)
json
Copy
Edit
{
  "metadata": {
    "documents": ["adobe_round 1A.pdf", "adobe_round 1B.pdf"],
    "persona": "PhD Researcher in Computational Biology",
    "job": "Prepare a literature review on graph neural networks",
    "timestamp": "2025-07-28 13:01:45"
  },
  "extracted_sections": [
    {
      "document": "adobe_round 1A.pdf",
      "page": 1,
      "section_title": "Graph Neural Networks Overview",
      "importance_rank": 1
    }
  ],
  "sub_section_analysis": [
    {
      "document": "adobe_round 1A.pdf",
      "page": 1,
      "refined_text": "Graph Neural Networks (GNNs) enable deep learning on non-Euclidean data structures..."
    }
  ]
}
⚙️ How It Works
inference.py loads PDFs + meta.json

Splits PDFs into text chunks (1-2 paragraphs)

Encodes using sentence-transformers

Ranks chunks based on cosine similarity to persona+job context

Returns top relevant chunks per document

🧱 Tech Stack
Python 3.10-slim

SentenceTransformers 5.0.0

PyMuPDF

Torch (CPU-only)

Docker (stateless execution)

