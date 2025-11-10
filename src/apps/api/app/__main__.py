"""Entrypoint for running the Container Base API service."""
import uvicorn

from .main import app


def main() -> None:
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )


if __name__ == "__main__":
    main()
