document.addEventListener("DOMContentLoaded", () => {
  // Input Step elements
  const photoInput = document.getElementById("photo-input");
  const cameraBtn = document.getElementById("camera-btn");
  const previewContainer = document.getElementById("preview-container");
  const photoPreview = document.getElementById("photo-preview");
  const clearPhotoBtn = document.getElementById("clear-photo-btn");
  const ingredientsInput = document.getElementById("ingredients-input");
  const analyzeBtn = document.getElementById("analyze-btn");

  // Loader & Error elements
  const loader = document.getElementById("loader");
  const loaderText = document.getElementById("loader-text");
  const errorCard = document.getElementById("error-card");
  const errorMessage = document.getElementById("error-message");
  const retryBtn = document.getElementById("retry-btn");

  // Refine Step elements
  const refineCard = document.getElementById("refine-card");
  const tagsContainer = document.getElementById("tags-container");
  const addTagInput = document.getElementById("add-tag-input");
  const addTagBtn = document.getElementById("add-tag-btn");
  const findRecipeBtn = document.getElementById("find-recipe-btn");

  // Output Step elements
  const recipeCard = document.getElementById("recipe-card");
  const recipeTitle = document.getElementById("recipe-title");
  const recipeIngredients = document.getElementById("recipe-ingredients");
  const recipeSteps = document.getElementById("recipe-steps");
  const recipePhoto = document.getElementById("recipe-photo");
  const photoPlaceholder = document.getElementById("photo-placeholder");
  const downloadBtn = document.getElementById("download-btn");

  let selectedFile = null;
  let ingredients = [];
  let currentRecipe = null; // Store recipe for download

  // --- Photo Input Handling ---
  cameraBtn.addEventListener("click", () => photoInput.click());

  photoInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) {
      selectedFile = file;
      const reader = new FileReader();
      reader.onload = (event) => {
        photoPreview.src = event.target.result;
        previewContainer.classList.remove("hidden");
      };
      reader.readAsDataURL(file);
    }
  });

  clearPhotoBtn.addEventListener("click", () => {
    selectedFile = null;
    photoInput.value = "";
    photoPreview.src = "";
    previewContainer.classList.add("hidden");
  });

  // --- Analyze Ingredients (Step 1) ---
  const triggerAnalysis = async () => {
    const queryText = ingredientsInput.value.trim();
    if (!selectedFile && !queryText) return;

    // Reset visibility
    recipeCard.classList.add("hidden");
    refineCard.classList.add("hidden");
    errorCard.classList.add("hidden");
    loaderText.textContent = "analyzing ingredients...";
    loader.classList.remove("hidden");
    analyzeBtn.disabled = true;

    const formData = new FormData();
    if (selectedFile) {
      formData.append("image", selectedFile);
    }
    if (queryText) {
      formData.append("text", queryText);
    }

    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        throw new Error("Analysis failed");
      }

      const data = await response.json();
      ingredients = data.ingredients || [];

      // Render tags
      renderTags();

      // Show Refine Section
      loader.classList.add("hidden");
      refineCard.classList.remove("hidden");
      refineCard.classList.add("fade-in");
    } catch (err) {
      console.error(err);
      loader.classList.add("hidden");
      errorCard.classList.remove("hidden");
      errorMessage.textContent = "The chef had trouble parsing your fridge. Try again?";
    } finally {
      analyzeBtn.disabled = false;
    }
  };

  analyzeBtn.addEventListener("click", triggerAnalysis);

  // --- Tag Rendering & Refinement (Step 2) ---
  const renderTags = () => {
    tagsContainer.innerHTML = "";
    ingredients.forEach((ingredient, index) => {
      const tag = document.createElement("div");
      tag.className = "tag";
      tag.textContent = ingredient;

      const removeBtn = document.createElement("button");
      removeBtn.className = "tag-remove";
      removeBtn.textContent = "×";
      removeBtn.addEventListener("click", () => {
        // Trigger exit animation before removing
        tag.style.transform = "scale(0.8)";
        tag.style.opacity = "0";
        setTimeout(() => {
          ingredients.splice(index, 1);
          renderTags();
        }, 150);
      });

      tag.appendChild(removeBtn);
      tagsContainer.appendChild(tag);
    });
  };

  // Add Tag manually
  const appendManualTag = () => {
    const value = addTagInput.value.trim().toLowerCase();
    if (value && !ingredients.includes(value)) {
      ingredients.push(value);
      renderTags();
      addTagInput.value = "";
    }
  };

  addTagBtn.addEventListener("click", appendManualTag);
  addTagInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      appendManualTag();
    }
  });

  // --- Generate Recipe (Step 3) ---
  const triggerRecipeGeneration = async () => {
    if (ingredients.length === 0) return;

    // Reset visibility
    recipeCard.classList.add("hidden");
    errorCard.classList.add("hidden");
    loaderText.textContent = "rescuing your ingredients...";
    loader.classList.remove("hidden");
    findRecipeBtn.disabled = true;

    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ ingredients: ingredients })
      });

      if (!response.ok) {
        throw new Error("Recipe generation failed");
      }

      const data = await response.json();
      currentRecipe = data.recipe;

      // Populate Recipe Text
      recipeTitle.textContent = data.recipe.title.toLowerCase();

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
      errorMessage.textContent = "The chef had trouble cooking. Try again?";
    } finally {
      findRecipeBtn.disabled = false;
    }
  };

  findRecipeBtn.addEventListener("click", triggerRecipeGeneration);

  // --- Save Offline (Markdown) ---
  downloadBtn.addEventListener("click", () => {
    if (!currentRecipe) return;

    const mdContent = `# ${currentRecipe.title}

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
