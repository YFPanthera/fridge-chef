# Fridge Chef — UX Design Doc

**Designer:** UX Designer
**Status:** Draft v0.1
**Last updated:** 2026-05-27

---

## 1. The design bet

We are betting that the "Zero-Waste Coach" personality is best felt through a tactile, comforting, and low-pressure interface. Rather than a busy kitchen grid, the entire experience centers around a single soft cloud-card containing the ingredients input. Once submitted, it resolves into a beautiful, shareable recipe card. The presence of the sleeping puppy mascot sets a calm, safe tone, reassuring the user that cooking with leftovers is low-stakes and cozy.

## 2. The defining interaction

User types their leftover ingredients in the clean text input and clicks "Cook Zero-Waste" (the glowing, apple-red pillowy button).
The button sinks slightly under the cursor. The text box dims, and a soft, pastel-peach loading shimmer ripples across the card while the sleeping puppy mascot displays a slow breathing animation.
After ~3.5s, the card expands downwards with a smooth, physics-like spring animation, revealing the recipe, a cost-saving badge, and the dish image fading in. Total time: ~4s. Feels like: a fresh batch of bread rising in the oven.

## 3. Screen inventory

The product is a single-screen responsive web application:

- **Fridge Chef Dashboard** — A single-screen portal containing the sleeping puppy hero mascot, the ingredient text input, and the dynamically generated recipe cloud-card.

## 4. Screen-by-screen specs

### Fridge Chef Dashboard

**Purpose:** The central workspace where the user inputs what's in their fridge and reads the generated recipe.

**Layout (top to bottom):**
1. **Puppy Mascot Hero** — The centered, non-negotiable sleeping puppy image (`/assets/cloud-pup-mascot.png`) with a slow breathing animation.
2. **Main Cloud-Card** — A large, pillowy-shadow card containing:
   - *Title & Subtitle* — Soft serif text ("Fridge Chef", "let's save your leftovers").
   - *Ingredient Input* — A single, pillowy text input field with a soft inset shadow. Placeholder: "stale sourdough, cheddar, half a tomato...".
   - *Action Button* — A pillowy, apple-red button labeled "Cook Zero-Waste".
3. **Recipe Card Area (Hidden initially)** — Automatically displays and reveals:
   - *Cost-Saving Badge* — A soft-peach pill badge highlighting the dollar value saved (e.g., "Saved $7.80").
   - *Dish Title & Recipe* — "Scrappy Sourdough Melt", list of used ingredients, and numbered cooking steps in soft ink.
   - *Dish Photo* — A rounded (24px radius) image container displaying the AI-generated dish photo.
   - *Download/Save Button* — A pill-shaped, ghost button labeled "Save Offline (Markdown)" with a download icon.

**Key interactions:**
- *Focus Input* → Glowing peach focus ring wraps the input.
- *Click Action Button* → Button triggers a soft click state, disables input, and starts the shimmer loader.
- *Recipe Loaded* → Receives output JSON and image; card expands; photo fades in.
- *Click Save Offline* → Triggers a browser file download of the recipe in Markdown format (including title, ingredients, steps, and cost-saving highlight) for offline viewing.

**States:**
- **Default:** Clean layout, mascot napping, input ready.
- **Empty / first-time:** No recipe card is visible below the input card. A soft-text tip reads: "Type a few things from your fridge to begin."
- **Loading:** Input card shimmers with a pastel-peach gradient, and the action button shows a "whispering..." state.
- **Error:** Card displays a gentle notice: "The chef is having a quick nap. Let's try again?" in soft red text.
- **Edge / "too much":** Long ingredient strings wrap cleanly within the input box; the output recipe card supports vertical scrolling with a custom soft-pill scrollbar.

## 5. The user journey

**First open:** The user arrives on the page. They see a soft sky gradient and the sleeping white puppy with a tiny apple on its head. The environment feels extremely warm and calm. The single card invites them to input their food scraps.

**First successful use:** The user types "wrinkled spinach, leftover rice, 1 egg" and clicks the apple-red button. The screen shimmers softly, maintaining the calm atmosphere. A few seconds later, the card expands down. A photo of a beautiful, warm "Golden Rice Bowl with Wilted Greens" fades in next to step-by-step instructions. At the top of the recipe, a little badge glows: "Saved $9.20". They feel a sense of relief and accomplishment.

**Second session:** The user returns the next day. The page is in its clean default state. They immediately know they can type their new leftovers here to get another zero-waste recommendation.

## 6. Component & visual notes

- **Typography:** Display headings use *Fraunces* (soft serif) for a friendly, editorial feel. Body text uses *Nunito* (rounded humanist sans) for a clean, accessible layout.
- **Color:** Soft sky-blue background gradient with warm peach sunray highlights bleeding through. The recipe card is a warm off-white (`--cloud-white`). The primary CTA button is a rich, warm apple-red (`--apple-red`).
- **Motion:** Micro-animations utilize a gentle overshoot cubic-bezier (`0.34, 1.56, 0.64, 1`). The puppy mascot has an ongoing 7s slow breathing loop.
- **The signature visual:** The sleeping white puppy mascot napping on a cloud with an apple on its head.
- **Microcopy voice:** Encouraging, lowercase, friendly zero-waste coaching (e.g., "rescuing your ingredients...", "look at what you saved!").

## 7. Accessibility & inclusion

- **Screen readers:** Interactive elements use clear `aria-label` tags (e.g., `aria-label="What is in your fridge?"`). The puppy mascot image includes an alternative description.
- **Motor difficulties:** Button and input targets have a minimum height of 56px with generous hitboxes.
- **Connectivity:** Uses a lightweight payload. If the image model call fails or times out, the text recipe is still displayed with a friendly, styled illustration placeholder instead of throwing a blank error.

## 8. What we are NOT designing

- **No Settings screen** — the default is optimized for zero-waste recommendations.
- **No History page** — only the current recipe is shown.
- **No customized themes** — the Cloud-Pup pastel sky theme is locked.

## 9. Open design questions

- [ ] Should we display the estimated cost saving as a prominent badge at the top of the recipe, or next to the dish photo? (Recommended: Prominent badge at the top of the recipe card).

## 10. Handoff to engineering

The recipe card expansion needs to be GPU-accelerated (using `transform` or CSS Grid `grid-template-rows` transitions) to prevent layout stutter. The dish photo must have a CSS loading blur-up effect so that the user doesn't see a blocky image loading in segments.
