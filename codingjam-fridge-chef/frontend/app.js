document.addEventListener("DOMContentLoaded", () => {
  const ingredientsInput = document.getElementById("ingredients-input");
  const generateBtn = document.getElementById("generate-btn");
  const loader = document.getElementById("loader");
  const errorCard = document.getElementById("error-card");
  const errorMessage = document.getElementById("error-message");
  const retryBtn = document.getElementById("retry-btn");
  const recipeCard = document.getElementById("recipe-card");
  const recipeTitle = document.getElementById("recipe-title");
  const recipeIngredients = document.getElementById("recipe-ingredients");
  const recipeSteps = document.getElementById("recipe-steps");
  const recipePhoto = document.getElementById("recipe-photo");
  const photoPlaceholder = document.getElementById("photo-placeholder");
  const costBadge = document.getElementById("cost-badge");
  const downloadBtn = document.getElementById("download-btn");

  let currentRecipe = null; // Store current generated recipe for download

  // Handle generation click
  const triggerGeneration = async () => {
    const query = ingredientsInput.value.trim();
    if (!query || query.length < 2) return;

    // Reset visibility
    recipeCard.classList.add("hidden");
    errorCard.classList.add("hidden");
    loader.classList.remove("hidden");
    generateBtn.disabled = true;

    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ ingredients: query })
      });

      if (!response.ok) {
        throw new Error("Server responded with error status");
      }

      const data = await response.json();
      currentRecipe = data.recipe;

      // Populate Recipe Text
      recipeTitle.textContent = data.recipe.title.toLowerCase();
      
      // Cost savings badge
      if (data.recipe.cost_saving_highlight) {
        costBadge.textContent = data.recipe.cost_saving_highlight.toLowerCase();
        costBadge.classList.remove("hidden");
      } else {
        costBadge.classList.add("hidden");
      }

      // Ingredients list
      recipeIngredients.innerHTML = "";
      data.recipe.ingredients.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        recipeIngredients.appendChild(li);
      });

      // Steps list
      recipeSteps.innerHTML = "";
      data.recipe.steps.forEach(step => {
        const li = document.createElement("li");
        li.textContent = step;
        recipeSteps.appendChild(li);
      });

      // Recipe Photo
      if (data.image_base64) {
        recipePhoto.src = data.image_base64;
        recipePhoto.classList.remove("hidden");
        photoPlaceholder.classList.add("hidden");
      } else {
        recipePhoto.classList.add("hidden");
        photoPlaceholder.classList.remove("hidden");
      }

      // Show recipe card
      loader.classList.add("hidden");
      recipeCard.classList.remove("hidden");
      recipeCard.classList.add("fade-in");
    } catch (err) {
      console.error(err);
      loader.classList.add("hidden");
      errorCard.classList.remove("hidden");
    } finally {
      generateBtn.disabled = false;
    }
  };

  generateBtn.addEventListener("click", triggerGeneration);
  retryBtn.addEventListener("click", triggerGeneration);

  // Trigger on Enter key
  ingredientsInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !generateBtn.disabled) {
      triggerGeneration();
    }
  });

  // Handle Download Recipe (Markdown)
  downloadBtn.addEventListener("click", () => {
    if (!currentRecipe) return;

    const mdContent = `# ${currentRecipe.title}
    
## Cost Savings
* **${currentRecipe.cost_saving_highlight}**

## What You'll Need
${currentRecipe.ingredients.map(item => `* ${item}`).join('\n')}

## How to Cook It
${currentRecipe.steps.map((step, idx) => `${idx + 1}. ${step}`).join('\n')}

---
Saved via Fridge Chef ☁️🐾`;

    const blob = new Blob([mdContent], { type: "text/markdown;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement("a");
    link.href = url;
    
    // Create clean filename from recipe title
    const filename = currentRecipe.title
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/(^-|-$)/g, "") + ".md";
      
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  });
});
