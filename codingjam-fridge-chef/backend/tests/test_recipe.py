import json
import pytest
import base64
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app, FALLBACK_IMAGE_B64

client = TestClient(app)

def test_analyze_validation_error():
    """Asserts that calling analyze without image or text returns a 400."""
    response = client.post("/api/analyze")
    assert response.status_code == 400

@patch("main._create_client")
def test_analyze_text_input(mock_create_client):
    """Verifies that text inputs are correctly sent to Gemini and parsed as ingredients."""
    mock_genai_client = MagicMock()
    mock_create_client.return_value = mock_genai_client

    # Mock response from gemini-3.5-flash for ingredients extraction
    mock_api_response = MagicMock()
    mock_api_response.text = json.dumps(["egg", "tomato", "cheddar"])
    mock_api_response.usage_metadata = MagicMock(prompt_token_count=100, candidates_token_count=30)
    mock_genai_client.models.generate_content.return_value = mock_api_response

    response = client.post("/api/analyze", data={"text": "egg, tomato, cheddar"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["ingredients"] == ["egg", "tomato", "cheddar"]
    assert "X-API-Cost" in response.headers

@patch("main._create_client")
def test_analyze_image_input(mock_create_client):
    """Verifies that uploaded images are successfully processed and return detected ingredients."""
    mock_genai_client = MagicMock()
    mock_create_client.return_value = mock_genai_client

    mock_api_response = MagicMock()
    mock_api_response.text = json.dumps(["spinach", "leftover rice"])
    mock_api_response.usage_metadata = MagicMock(prompt_token_count=150, candidates_token_count=40)
    mock_genai_client.models.generate_content.return_value = mock_api_response

    # Create dummy PNG image bytes using PIL
    from PIL import Image
    import io
    img = Image.new('RGB', (10, 10), color = 'red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    dummy_image = img_byte_arr.getvalue()
    
    files = {"image": ("fridge.png", dummy_image, "image/png")}
    response = client.post("/api/analyze", files=files)
    assert response.status_code == 200
    
    data = response.json()
    assert data["ingredients"] == ["spinach", "leftover rice"]
    assert "X-API-Cost" in response.headers

def test_recipe_json_cleanup():
    """Tests the markdown code fence clean-up logic."""
    from main import clean_json_response
    raw_response = "```json\n{\n  \"title\": \"scrappy soup\",\n  \"ingredients\": [\"scraps\"],\n  \"steps\": [\"boil\"]\n}\n```"
    cleaned = clean_json_response(raw_response)
    data = json.loads(cleaned)
    assert data["title"] == "scrappy soup"
    assert data["ingredients"] == ["scraps"]
    assert data["steps"] == ["boil"]

@patch("main._create_client")
def test_fallback_image_on_generation_failure(mock_create_client):
    """Verifies that when image generation fails, the fallback image is returned."""
    mock_genai_client = MagicMock()
    mock_create_client.return_value = mock_genai_client

    # First call: Recipe generation succeeds (no cost badge / savings field)
    mock_text_response = MagicMock()
    mock_text_response.text = json.dumps({
        "title": "scrappy grilled cheese",
        "ingredients": ["bread", "cheese"],
        "steps": ["toast it"]
    })
    mock_text_response.usage_metadata = MagicMock(prompt_token_count=100, candidates_token_count=50)

    # Second call: Image generation raises an exception
    mock_genai_client.models.generate_content.side_effect = [
        mock_text_response,
        Exception("Image model quota exceeded")
    ]

    response = client.post("/api/generate", json={"ingredients": ["bread", "cheese"]})
    assert response.status_code == 200
    
    data = response.json()
    assert data["recipe"]["title"] == "scrappy grilled cheese"
    assert data["image_base64"] == FALLBACK_IMAGE_B64

@patch("main._create_client")
def test_full_two_step_flow(mock_create_client):
    """Full integration test of the two-step flow: analyze followed by generate."""
    mock_genai_client = MagicMock()
    mock_create_client.return_value = mock_genai_client

    # Step 1 Mock: Analyze image
    mock_analyze_response = MagicMock()
    mock_analyze_response.text = json.dumps(["egg", "tomato"])
    mock_analyze_response.usage_metadata = MagicMock(prompt_token_count=80, candidates_token_count=20)

    # Step 2 Mocks: Generate recipe and generate image
    mock_text_response = MagicMock()
    mock_text_response.text = json.dumps({
        "title": "Tomato Egg Scramble",
        "ingredients": ["1 egg", "1 tomato"],
        "steps": ["cook together"]
    })
    mock_text_response.usage_metadata = MagicMock(prompt_token_count=120, candidates_token_count=80)

    mock_image_response = MagicMock()
    mock_part = MagicMock()
    mock_part.inline_data = MagicMock(data=b"fake_png_bytes")
    mock_image_response.parts = [mock_part]

    # Chain side effects: 1 call to analyze, 2 calls to generate (recipe then image)
    mock_genai_client.models.generate_content.side_effect = [
        mock_analyze_response, # Call in POST /api/analyze
        mock_text_response,    # Call 1 in POST /api/generate
        mock_image_response    # Call 2 in POST /api/generate
    ]

    # 1. Trigger Analyze
    response1 = client.post("/api/analyze", data={"text": "egg, tomato"})
    assert response1.status_code == 200
    ingredients = response1.json()["ingredients"]
    assert ingredients == ["egg", "tomato"]

    # 2. Trigger Generate
    response2 = client.post("/api/generate", json={"ingredients": ingredients})
    assert response2.status_code == 200
    
    data = response2.json()
    assert data["recipe"]["title"] == "Tomato Egg Scramble"
    assert data["recipe"]["ingredients"] == ["1 egg", "1 tomato"]
    expected_b64 = base64.b64encode(b"fake_png_bytes").decode()
    assert expected_b64 in data["image_base64"]
    assert "X-API-Cost" in response2.headers
