"""Fridge Chef — FastAPI backend + Gemini AI integration."""

import json
import os
import base64
import io
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT

load_dotenv()

app = FastAPI(title="Fridge Chef")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class GenerateRequest(BaseModel):
    ingredients: str = Field(..., min_length=2, description="List of ingredients in the fridge")

class RecipeResponse(BaseModel):
    title: str
    ingredients: list[str]
    steps: list[str]
    cost_saving_highlight: str

# Cozy fallback SVG illustration in Cloud-Pup colors
FALLBACK_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
  <rect width="100%" height="100%" fill="#DCE7F5"/>
  <circle cx="200" cy="180" r="100" fill="#FBFAF7" opacity="0.9"/>
  <!-- Cozy soup bowl representing zero-waste cooking -->
  <path d="M130 180 h140 v20 a70 70 0 0 1 -140 0 z" fill="#E8B8A0"/>
  <rect x="120" y="170" width="160" height="10" rx="5" fill="#3A4A5C"/>
  <path d="M160 140 q20-20 0-40" stroke="#3A4A5C" stroke-width="6" fill="none" stroke-linecap="round"/>
  <path d="M200 140 q20-20 0-40" stroke="#3A4A5C" stroke-width="6" fill="none" stroke-linecap="round"/>
  <path d="M240 140 q20-20 0-40" stroke="#3A4A5C" stroke-width="6" fill="none" stroke-linecap="round"/>
  <!-- The single warm accent - apple-red splash -->
  <circle cx="200" cy="210" r="12" fill="#D4675B"/>
  <text x="200" y="320" font-family="'Fraunces', 'Nunito', serif" font-size="22" font-weight="bold" fill="#3A4A5C" text-anchor="middle">cozy zero-waste cooking</text>
  <text x="200" y="350" font-family="'Nunito', sans-serif" font-size="14" fill="#6B7A8A" text-anchor="middle">photo napping, but recipe is ready!</text>
</svg>"""

FALLBACK_IMAGE_B64 = "data:image/svg+xml;base64," + base64.b64encode(FALLBACK_SVG.encode()).decode()

def _create_client():
    """Create a fresh Gemini client for each request."""
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return genai.Client(api_key=api_key)
    # Default to Vertex AI mode or fallback to empty client
    return genai.Client(
        vertexai=True,
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )

def estimate_cost(prompt_tokens: int, candidate_tokens: int, images_generated: int) -> float:
    """Calculate the API cost of the generation request."""
    # Pricing:
    # gemini-3.5-flash: $0.075 / 1M input tokens, $0.30 / 1M output tokens
    # gemini-3.1-flash-image-preview: $0.03 per image
    input_cost = (prompt_tokens / 1_000_000) * 0.075
    output_cost = (candidate_tokens / 1_000_000) * 0.30
    image_cost = images_generated * 0.03
    return input_cost + output_cost + image_cost

@app.post("/api/generate")
async def generate(request: GenerateRequest, response: Response):
    """Generate a zero-waste recipe and image from input ingredients."""
    ingredients_text = request.ingredients.strip()[:1000]

    # Initialize client
    client = _create_client()

    # Step 1: Call gemini-3.5-flash for structured recipe text
    recipe_prompt = f"Here is what is in my fridge:\n{ingredients_text}\n\nGenerate a zero-waste recipe. Remember, output valid JSON only."
    
    prompt_tokens = 0
    candidate_tokens = 0
    images_generated = 0
    recipe_data = None

    try:
        text_response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=[
                {
                    "role": "user",
                    "parts": [{"text": SYSTEM_PROMPT + "\n\n" + recipe_prompt}],
                }
            ],
            config=types.GenerateContentConfig(
                temperature=0.7,
                response_mime_type="application/json",
            ),
        )
        
        # Track tokens
        if text_response.usage_metadata:
            prompt_tokens += text_response.usage_metadata.prompt_token_count or 0
            candidate_tokens += text_response.usage_metadata.candidates_token_count or 0

        # Parse JSON
        response_text = text_response.text.strip()
        # Clean markdown code fences if outputted
        if response_text.startswith("```"):
            response_text = response_text.split("\n", 1)[1]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()

        recipe_data = json.loads(response_text)
        
        # Validate schema fields
        for field in ["title", "ingredients", "steps", "cost_saving_highlight"]:
            if field not in recipe_data:
                raise ValueError(f"Missing required field '{field}' in AI response")

    except Exception as e:
        print(f"Recipe generation error: {e}")
        raise HTTPException(
            status_code=500,
            detail="The recipe chef is currently napping. Please try again in a bit!"
        )

    # Step 2: Call gemini-3.1-flash-image-preview for the dish image
    image_b64 = FALLBACK_IMAGE_B64
    image_prompt = (
        f"A beautiful, warm, organic food photography close-up shot of: {recipe_data['title']}. "
        f"Featuring these ingredients: {', '.join(recipe_data['ingredients'])}. "
        "Served on a lovely rustic plate. Soft lighting, cozy warm colors, shallow depth of field. "
        "No text, no labels, no hands. Soft cloudcore atmosphere."
    )

    try:
        image_response = client.models.generate_content(
            model="gemini-3.1-flash-image-preview",
            contents=[image_prompt],
        )
        images_generated += 1

        # Extract image bytes
        image_bytes = None
        for part in image_response.parts:
            if part.inline_data is not None:
                image_bytes = part.inline_data.data
                break
            # Fallback if as_image is available
            try:
                img = part.as_image()
                if img:
                    buffered = io.BytesIO()
                    img.save(buffered, format="PNG")
                    image_bytes = buffered.getvalue()
                    break
            except Exception:
                pass

        if image_bytes:
            image_b64 = "data:image/png;base64," + base64.b64encode(image_bytes).decode()
        else:
            print("No image parts found in model response. Using fallback.")

    except Exception as e:
        print(f"Image generation error (using fallback): {e}")
        # Soft fallback - we still want to return the recipe!
        image_b64 = FALLBACK_IMAGE_B64

    # Calculate and set cost headers
    total_cost = estimate_cost(prompt_tokens, candidate_tokens, images_generated)
    response.headers["X-API-Cost"] = f"${total_cost:.5f}"

    return {
        "recipe": recipe_data,
        "image_base64": image_b64
    }

@app.get("/api/health")
async def health():
    """Health check."""
    return {"status": "cozy"}

# Mount frontend static files
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
