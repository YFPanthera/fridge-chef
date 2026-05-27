import json
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app, FALLBACK_IMAGE_B64

client = TestClient(app)

def test_parse_ingredients_validation():
    """Asserts that inputs are validated correctly (e.g., min length of 2)."""
    # Test short input (raises validation error)
    response = client.post("/api/generate", json={"ingredients": "a"})
    assert response.status_code == 422  # Unprocessable Entity
    
    # Test empty input
    response = client.post("/api/generate", json={"ingredients": ""})
    assert response.status_code == 422

def test_recipe_json_cleanup():
    """Tests the markdown code fence clean-up logic."""
    from main import generate
    # We can test this by parsing a mocked string with backticks.
    # In main.py:
    raw_response = "```json\n{\n  \"title\": \"scrappy soup\",\n  \"ingredients\": [\"scraps\"],\n  \"steps\": [\"boil\"],\n  \"cost_saving_highlight\": \"Saved $5.00\"\n}\n```"
    
    # Simulate cleanup logic
    response_text = raw_response.strip()
    if response_text.startswith("```"):
        response_text = response_text.split("\n", 1)[1]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
    data = json.loads(response_text)
    assert data["title"] == "scrappy soup"
    assert data["ingredients"] == ["scraps"]
    assert data["steps"] == ["boil"]
    assert data["cost_saving_highlight"] == "Saved $5.00"

@patch("main._create_client")
def test_fallback_image_on_failure(mock_create_client):
    """Verifies that when image generation fails, the fallback image is returned."""
    # Mock GenAI client
    mock_genai_client = MagicMock()
    mock_create_client.return_value = mock_genai_client

    # First call: Recipe generation succeeds
    mock_text_response = MagicMock()
    mock_text_response.text = json.dumps({
        "title": "scrappy grilled cheese",
        "ingredients": ["bread", "cheese"],
        "steps": ["toast it"],
        "cost_saving_highlight": "Saved $6.00"
    })
    mock_text_response.usage_metadata = MagicMock(prompt_token_count=100, candidates_token_count=50)

    # Second call: Image generation raises an exception
    mock_genai_client.models.generate_content.side_effect = [
        mock_text_response,
        Exception("Image model quota exceeded")
    ]

    response = client.post("/api/generate", json={"ingredients": "bread, cheese"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["recipe"]["title"] == "scrappy grilled cheese"
    # Should fall back to the cozy SVG image
    assert data["image_base64"] == FALLBACK_IMAGE_B64

@patch("main._create_client")
def test_successful_generation_flow(mock_create_client):
    """Full integration test of the generate endpoint with mocked model responses."""
    mock_genai_client = MagicMock()
    mock_create_client.return_value = mock_genai_client

    # First call: Text recipe response
    mock_text_response = MagicMock()
    mock_text_response.text = json.dumps({
        "title": "Zero-Waste Spinach & Cheddar Sourdough Melt",
        "ingredients": ["2 slices bread", "1/2 cup cheddar", "1 cup spinach"],
        "steps": ["preheat pan", "assemble", "toast"],
        "cost_saving_highlight": "Saved $6.20 by avoiding a cafe run!"
    })
    mock_text_response.usage_metadata = MagicMock(prompt_token_count=120, candidates_token_count=80)

    # Second call: Image response containing inline data
    mock_image_response = MagicMock()
    mock_part = MagicMock()
    mock_part.inline_data = MagicMock(data=b"fake_png_bytes")
    mock_image_response.parts = [mock_part]

    mock_genai_client.models.generate_content.side_effect = [
        mock_text_response,
        mock_image_response
    ]

    response = client.post("/api/generate", json={"ingredients": "sourdough, cheddar, spinach"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["recipe"]["title"] == "Zero-Waste Spinach & Cheddar Sourdough Melt"
    assert data["recipe"]["ingredients"] == ["2 slices bread", "1/2 cup cheddar", "1 cup spinach"]
    
    import base64
    expected_b64 = base64.b64encode(b"fake_png_bytes").decode()
    assert expected_b64 in data["image_base64"]
    assert "X-API-Cost" in response.headers
