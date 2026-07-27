from fastapi import FastAPI

app = FastAPI(title="RagBot 2.0")

@app.get("/test")
async def test():
    return {"message": "testing successful"}
