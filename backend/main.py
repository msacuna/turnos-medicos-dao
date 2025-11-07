from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"mensaje": "API funcionando 🚀"}