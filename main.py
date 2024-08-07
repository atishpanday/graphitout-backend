from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import upload_file, fetch_data_chunks, fetch_plot_data, delete_file

server = FastAPI(root_path="/api")

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

server.include_router(upload_file.router)
server.include_router(fetch_data_chunks.router)
server.include_router(fetch_plot_data.router)
server.include_router(delete_file.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(server, host="0.0.0.0", port=8000)
