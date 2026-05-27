# Fridge Chef — UX Design Doc

**Designer:** UX Designer
**Status:** Draft v0.2
**Last updated:** 2026-05-27

---

## 1. The design bet

We are betting that giving users final control over their ingredients list makes the AI recipe feel more trusted and reliable. Rather than a pure black-box generation, we use a two-step interface: first, users capture their ingredients (via photo upload or typing); second, they refine the detected list in a friendly tag editor before generating the recipe. The Cloud-Pup aesthetic (pastel colors, rounded pill-tags, and the sleeping puppy mascot) keeps this process feeling interactive and pleasant.

## 2. The defining interaction

### Step 1: Analyze Ingredients
User uploads a photo of their fridge (or types items) and clicks "Analyze Ingredients". The card shows a soft shimmer.

### Step 2: Refine Tags
After ~2s, the identified ingredients appear as bubbly, soft-peach pill tags inside the card.
- User can click the "×" on any tag to remove it (it disappears with a soft fade-out).
- User can type a new ingredient in the input box and press Enter to append it as a new tag.

### Step 3: Generate Recipe
Once satisfied, the user clicks "Find Recipe" (the apple-red pillowy button). The card expands downwards with a spring animation, revealing the recipe and the dish photo fading in. Feels like: picking ingredients off a shelf and cooking them.

## 3. Screen inventory

The product is a single-screen responsive web application:

- **Fridge Chef Dashboard** — A single-screen portal that transitions through the upload step, the tag refinement step, and the recipe display.

## 4. Screen-by-screen specs

### Fridge Chef Dashboard

**Purpose:** The central workspace where the user captures, refines, and views their zero-waste recipe.

**Layout (top to bottom):**
1. **Puppy Mascot Hero** — The centered sleeping puppy image (`/assets/cloud-pup-mascot.png`) with a slow breathing animation.
2. **Main Cloud-Card** — A large, pillowy-shadow card containing:
   - *Title & Subtitle* — "Fridge Chef", "let's save your leftovers".
   - *Input Controls* — File/Image upload button (with preview thumbnail once selected) and a manual text input.
   - *Primary CTA* — "Analyze Ingredients" (pill-shaped button).
3. **Refine Section (Hidden initially, appears after analysis)**:
   - *Subheading* — "confirm what we're cooking with:"
   - *Tags Area* — A flex container of rounded tags (`border-radius: 9999px`) in soft-peach with "×" buttons.
   - *Add Ingredient Field* — A small, pill-shaped text input to quickly append new items.
   - *Action Button* — The primary apple-red button: "Find Recipe".
4. **Recipe Card Area (Hidden initially, appears after recipe generation)**:
   - *Dish Title & Recipe* — "Scrappy Spinach Scramble", ingredients list, and cooking steps.
   - *Dish Photo* — A rounded (24px radius) image container displaying the AI-generated dish photo.
   - *Save Button* — A pill-shaped ghost button: "Save Offline (Markdown)".

**Key interactions:**
- *Focus Input* → Glowing peach focus ring wraps active inputs.
- *Remove Tag* → Clicking a tag's "×" removes the tag from the active list.
- *Click Find Recipe* → Card shimmers, disables tag editing, and reveals the recipe on load.
- *Click Save Offline* → Triggers a browser file download of the recipe in Markdown format.

**States:**
- **Default:** Mascot napping, image upload and text inputs ready.
- **Refinement State:** Upload elements are collapsed; the card displays the bubbly tags list and the "Find Recipe" button.
- **Loading:** Shimmer animation ripples across the main card during analysis or recipe generation.
- **Error:** Card displays a gentle red message: "The chef is having a quick nap. Let's try again?"

## 5. The user journey

**First open:** The user opens the app, seeing the soft sky gradient and the sleeping white puppy. They click the camera button, snap a photo of their messy fridge shelf, and click "Analyze Ingredients".

**Refining ingredients:** The app shimmers and outputs four tags: `eggs`, `spinach`, `milk`, and `moldy cheese`. The user taps the `×` on `moldy cheese` to remove it. They type `onion` into the add-input, creating a new `onion` tag. They are happy with the list.

**Recipe generation:** The user clicks the apple-red "Find Recipe" button. The card expands, revealing a recipe for a "Spinach and Onion Frittata" along with a beautiful photo of the dish. They click the "Save Offline" button to save it to their downloads folder.

## 6. Component & visual notes

- **Typography:** Display headings use *Fraunces* (serif) for a friendly feel. Body text uses *Nunito* (rounded sans).
- **Color:** Soft sky-blue background gradient with peach highlights. Recipe card uses `--cloud-white`. Accent CTA is `--apple-red`. Bubbly tags use `--peach-whisper` fill with `--ink-deep` text.
- **Motion:** Micro-animations utilize a overshoot cubic-bezier (`0.34, 1.56, 0.64, 1`). The mascot has a slow breathing loop.
- **The signature visual:** The napping puppy mascot and the bubbly, popping tags.
- **Microcopy voice:** Encouraging, lowercase, friendly zero-waste coaching (e.g. "what did we find?", "let's cook this...").

## 7. Accessibility & inclusion

- **Screen readers:** Accessible labels for file uploads (`aria-label="Upload photo of your fridge"`). Tags have screen-reader labels (e.g. "Remove eggs").
- **Motor difficulties:** Tag close buttons are styled with generous hitboxes to ensure ease of tapping on mobile.

## 8. What we are NOT designing

- **No Cost-Saving badge** — removed from the layout.
- **No History page** — only current session recipe is shown.
- **No manual photo-cropping tools** — we pass the image as-is to Gemini.

## 9. Open design questions

- [ ] Should the text input be completely hidden once a photo is uploaded, or should they be side-by-side? (Recommended: Side-by-side or stacked so the user can choose how they want to start).

## 10. Handoff to engineering

The tag removal should trigger a standard CSS transition (e.g. `transform: scale(0.9); opacity: 0;` over 200ms) to make the "pop" animation feel tactile.
