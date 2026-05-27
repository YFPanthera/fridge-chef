# Fridge Chef — Product Design Doc

**Author:** PM
**Status:** Draft v0.1
**Last updated:** 2026-05-27
**One-liner:** Input your random leftover ingredients and get a customized, cost-saving recipe with an AI-generated dish photo.

---

## 1. The user & the moment

Who is this for, and what are they doing/feeling **right before** they open the app?

- **Who:** A budget-conscious, busy home cook who hates wasting food and wants to save money.
- **When:** It is 7 PM on a Wednesday. They are staring into the fridge, exhausted after work, seeing only a random assortment of leftovers (e.g., half-wilted spinach, a block of cheddar, stale bread). They are tempted to order expensive takeout but feel guilty about both the cost and letting the food go to waste.
- **Why now:** Food inflation has made grocery prices soar. Meanwhile, modern recipe apps assume a fully stocked pantry and send users on grocery store runs, rather than helping them use what they already have.

## 2. The contract (I/O)

The most important section. What does the user give, and what do they get back?

- **Input:** A single, clean text input box answering the prompt: "What's in your fridge?" (e.g., "stale sourdough, cheddar, half a tomato").
- **Output:** A beautiful cloud-pup recipe card containing a Title, ingredients used, simple step-by-step instructions, a Cost-Saving Highlight estimating the money saved, and an AI-generated photo of the completed dish.
- **The loop:** One-shot generation. Open app → input ingredients → tap generate → receive recipe card + photo.

## 3. The magical moment

The single sentence the user would say to a friend after using this for the first time. Write it in their voice.

> "I typed in my half-empty box of spinach and stale bread, and it actually gave me a gourmet grilled cheese recipe and showed me I saved $8!"

## 4. Scope: what we ARE building (v1)

The minimum surface area. Each bullet is a thing a user can do or see.

- A single-screen UI featuring the signature sleeping puppy mascot.
- A clean, simple text input box for ingredient lists.
- An "apple-variant" primary action button to generate the recipe. (Note: "apple-variant" refers to using the Cloud-Pup signature warm accent color `--apple-red` to draw attention to the primary CTA).
- A display card showing the generated recipe (title, ingredients list, step-by-step instructions).
- A Cost-Saving Highlight showing estimated food waste/money saved. (Note: Since we are not using a complex price database, the Gemini model will estimate a reasonable dollar value saved based on the specific ingredients rescued compared to ordering takeout).
- An AI-generated dish photo integrated into the recipe card.

## 5. Scope: what we are NOT building

The cuts ARE the product. List the obvious things people will ask for that we're explicitly NOT doing in v1.

- **No grocery store mapping / shopping lists** — out of scope; we are only using what is already in the fridge.
- **No dietary filters (vegan, gluten-free, etc.)** — users specify their dietary needs directly in the ingredient text input if they wish.
- **No user accounts / logins** — all recipe histories (if any) or states are device-local to minimize friction.
- **No recipe bookmarking / saving database** — users can screenshot the beautiful card if they want to save it.
- **No meal planners or calendar views** — out of scope for a simple one-shot chef assistant.

## 6. The signature detail

The culinary voice of the AI is a **Zero-Waste Coach** that uses the soft, pastel "Cloud-Pup" visual style.
The mascot is a painterly sleeping white puppy curled into a cloud with a tiny red apple resting on its head, breathing gently at the top of the screen. The AI's tone is encouraging, extremely budget-focused, and congratulatory about using leftovers. When the recipe is generated, the Cost-Saving Highlight is highlighted in the center of the card as a little glowing green badge saying "You saved approximately $7.50 by not ordering takeout!"

## 7. Success: how we know it worked

Pick ONE primary signal.

- **Primary:** &ge;40% of users who generate their first recipe come back to generate a second one within 7 days.
- **What we're NOT measuring:** Total page views, average time spent on page.

## 8. Open questions

Real unknowns that need answers before/during build.

- [ ] Will the latency of generating both the recipe text and the dish image in sequence exceed our p95 latency budget of 5s?
- [ ] How do we calculate a realistic "Cost-Saving Highlight" value without a complex price database? (Resolved: The LLM will estimate this in its structured JSON output).

## 9. Handoff

- **For UX:** The transition between submitting the input and displaying the loading screen needs to maintain the calm, "sleeping puppy" atmosphere without looking like the app froze.
- **For Eng:** Running consecutive Gemini calls (one for recipe generation and one for image generation) within a tight latency budget is our main technical hurdle. We will mitigate costs and latency by using the fastest available models: `gemini-3.5-flash` for the recipe text and `gemini-3.1-flash-image-preview` for the dish photo.
