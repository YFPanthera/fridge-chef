# Fridge Chef — Product Design Doc

**Author:** PM
**Status:** Draft v0.3
**Last updated:** 2026-05-27
**One-liner:** Snap a photo of your fridge leftovers (or type them), refine the detected ingredients list, and get a customized recipe with an AI-generated dish photo.

---

## 1. The user & the moment

Who is this for, and what are they doing/feeling **right before** they open the app?

- **Who:** A budget-conscious, busy home cook who hates wasting food and wants to save money.
- **When:** It is 7 PM on a Wednesday. They are standing in front of their open fridge, exhausted after work, seeing only a random, messy assortment of food scraps. They want an easy way to scan what they have, but want the final say on what goes into their meal (e.g. omitting an ingredient they don't feel like eating today).
- **Why now:** Purely automated recipes can include ingredients the user wants to avoid or misidentify items in the photo. A two-step workflow (Detect → Refine → Generate) gives the user absolute control while still removing the typing overhead.

## 2. The contract (I/O)

The most important section. What does the user give, and what do they get back?

- **Input**:
  - Step 1: An uploaded image/camera snap of the fridge interior (PNG/JPEG/WEBP), or manual text input.
  - Step 2: An editable list of ingredients where the user can add, delete, or refine items.
- **Output:** A beautiful cloud-pup recipe card containing the recipe Title, ingredients used, step-by-step instructions, and an AI-generated photo of the dish.
- **The loop:**
  1. Open app → upload/take photo (or type initial ingredients).
  2. View detected ingredients in an editable list.
  3. Refine the list (remove, edit, or add items).
  4. Tap "Find Recipe" → receive recipe card + generated dish photo.

## 3. The magical moment

The single sentence the user would say to a friend after using this for the first time. Write it in their voice.

> "I just took a photo of my fridge, it listed all my veggies, I unchecked the broccoli because I wanted to save it for tomorrow, and it made me the perfect spinach omelet!"

## 4. Scope: what we ARE building (v1)

The minimum surface area. Each bullet is a thing a user can do or see.

- A single-screen UI featuring the signature sleeping puppy mascot.
- A file uploader/camera button to snap or select a fridge photo.
- An intermediate "Refine Ingredients" view where ingredients are displayed as tags that can be deleted (tapped to remove), edited, or manually added.
- A clean, simple text input box to manually type ingredients (either to start or to add to the list).
- An "apple-variant" primary action button to generate the recipe. (Note: "apple-variant" refers to using the Cloud-Pup signature warm accent color `--apple-red` to draw attention to the primary CTA).
- A display card showing the generated recipe (title, ingredients list, step-by-step instructions).
- An AI-generated dish photo integrated into the recipe card.
- A button to download/save the generated recipe card locally as a Markdown file.

## 5. Scope: what we are NOT building

The cuts ARE the product. List the obvious things people will ask for that we're explicitly NOT doing in v1.

- **No server-side recipe history database** — all data is client-side and transient.
- **No Cost-Saving Highlight** — we are excluding price/saving calculations to focus purely on recipe quality and ingredient control.
- **No grocery store mapping / shopping lists** — out of scope.
- **No dietary filters (vegan, gluten-free, etc.)** — users refine the ingredient list manually to suit their dietary requirements.
- **No user accounts / logins** — all actions are local and anonymous.

## 6. The signature detail

The culinary voice of the AI is a **Zero-Waste Coach** that uses the soft, pastel "Cloud-Pup" visual style.
The mascot is a painterly sleeping white puppy curled into a cloud with a tiny red apple resting on its head, breathing gently at the top of the screen. The AI's tone is encouraging, lowercase, and friendly. When the ingredients are detected, they appear as bubbly, cloud-like tag pills that the user can dismiss with a soft "pop" animation.

## 7. Success: how we know it worked

Pick ONE primary signal.

- **Primary:** &ge;40% of users who generate their first recipe come back to generate a second one within 7 days.
- **What we're NOT measuring:** Total page views, average time spent on page.

## 8. Open questions

Real unknowns that need answers before/during build.

- [ ] Will the two-step request flow (multimodal extract call followed by recipe generation call) increase total interaction time significantly?
- [ ] How do we design the tag-editing interface to feel spacious and easy to use on mobile devices?

## 9. Handoff

- **For UX:** The transition between photo upload, ingredient extraction, and the refinement view needs to feel cohesive and clear so the user knows they are expected to review the list.
- **For Eng:** We need to handle image uploads and extract a clean list of ingredients in JSON. We will use `gemini-3.5-flash` for ingredient extraction and recipe generation, and `gemini-3.1-flash-image-preview` for the final dish photo.
