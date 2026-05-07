"""Thin client for Luma Labs Dream Machine uni-1 image generation API."""

import os
import time
import requests
from typing import Optional

API_BASE = "https://api.lumalabs.ai/dream-machine/v1/generations"


class LumaClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("LUMALABS_API_KEY")
        if not self.api_key:
            raise ValueError("LUMALABS_API_KEY not set")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })

    def generate_image(self, prompt: str, aspect_ratio: str = "1:1",
                       model: str = "uni1") -> dict:
        """Submit an image generation request. Returns the generation object."""
        resp = self.session.post(
            f"{API_BASE}/image",
            json={
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "model": model,
            },
        )
        resp.raise_for_status()
        return resp.json()

    def poll_until_complete(self, generation_id: str, timeout: int = 120,
                           interval: int = 3) -> dict:
        """Poll generation status until complete or timeout."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            resp = self.session.get(f"{API_BASE}/{generation_id}")
            resp.raise_for_status()
            data = resp.json()
            status = data.get("state", data.get("status", ""))
            if status in ("completed", "succeeded"):
                return data
            if status in ("failed", "error"):
                raise RuntimeError(f"Generation failed: {data}")
            time.sleep(interval)
        raise TimeoutError(f"Generation {generation_id} timed out after {timeout}s")

    def download_image(self, url: str, output_path: str) -> str:
        """Download generated image to local path."""
        resp = requests.get(url, stream=True)
        resp.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)
        return output_path
