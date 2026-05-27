# Fridge Chef ☁️🐾

A soft, cozy, zero-waste recipe assistant built using the **Cloud-Pup** design aesthetic and powered by **Google Gemini**.

---

## What This App Does
**Fridge Chef** rescues your leftover ingredients and turns them into single-page gourmet, cost-saving recipes.
1. **Input**: Type whatever scraps you have left in your fridge (e.g., "half-used onion, stale bread, cheese").
2. **Output**: The app generates a customized recipe (Title, Ingredients, Instructions), an estimated Cost-Saving Highlight showing how much money you saved by not ordering takeout, and an AI-generated dish photo.
3. **Offline Saving**: You can download the completed recipe as a Markdown file directly to your local computer with one click, ensuring you can still access it if your internet drops.

---

## Project Structure
```
├── product.md            # Product requirements, core loop, and success metrics
├── ui.md                 # UX wireframe layout, interactive states, and typography/colors
├── engineering.md        # Technical architecture, endpoints, and testing strategy
└── codingjam-fridge-chef/
    ├── backend/          # FastAPI Python application and Gemini SDK service
    └── frontend/         # HTML/CSS/JS files and Cloud-Pup asset files
```

---

## Installation & Setup

Ensure you have [uv](https://github.com/astral-sh/uv) and [git](https://git-scm.com/) installed on your machine.

### 1. Configure the Environment
Navigate to the backend directory and create a `.env` file:
```bash
cd codingjam-fridge-chef/backend
touch .env
```
Add your Gemini API Key:
```env
GEMINI_API_KEY=your-gemini-api-key-here
```
> **Note**: Image generation requires a Google Cloud project with **billing enabled** (pay-as-you-go tier). If your key is on the free tier, the app will gracefully display a beautiful, custom zero-waste fallback illustration instead of throwing an error.

### 2. Install Dependencies
Run `uv sync` to set up the Python virtual environment and install all packages:
```bash
uv sync
```

---

## Running the App

### Start the Development Server
From the `backend/` directory, start Uvicorn:
```bash
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8080
```
Open your browser and navigate to:
👉 **[http://127.0.0.1:8080](http://127.0.0.1:8080)**

---

## Running the Tests
To run unit and integration tests (which mock all Gemini API calls to run deterministically and free of charge), navigate to the `backend/` directory and execute:
```bash
uv run pytest -v
```

---

## Design System & Source of Truth
We adhere to a strict planning and specification protocol. The following files are the ultimate source of truth for the product requirements, design guidelines, and system architecture:
*   [**product.md**](file:///Users/yinkatj/Documents/antigravity/valiant-hertz/product.md): Explains the user story, magical moments, and project scope boundaries.
*   [**ui.md**](file:///Users/yinkatj/Documents/antigravity/valiant-hertz/ui.md): Specifies the visual components, Cloud-Pup color scheme, fonts, and animation easings.
*   [**engineering.md**](file:///Users/yinkatj/Documents/antigravity/valiant-hertz/engineering.md): Maps out the data models, API endpoints, testing plan, and trade-offs.
