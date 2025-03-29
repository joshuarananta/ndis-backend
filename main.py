from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
import fitz  # PyMuPDF for PDF processing

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the NDIS backend!"}

# Favicon endpoint
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("path/to/your/favicon.ico")

# Upload file endpoint
@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_path = f"uploaded_{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Process the PDF and extract text
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
            return {"filename": file.filename, "text": text}
        else:
            return {"filename": file.filename, "message": "File is not a PDF"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text
