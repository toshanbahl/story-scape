# Stage 12 – Responsive and accessibility pass

## What was done
- Every button and input is at least 44px tall, with an 8px radius and 16px text.
- A dark 3px **focus ring** shows keyboard users where they are.
- Every image has a caption, which screen readers read as the description.
- Every input has a visible label, not just a placeholder.
- On screens under 640px wide, columns stack and the side gutter is 16px.
- Errors are written in plain words and say how to fix them.

## AI's role vs mine
| AI (Claude) | Me |
|---|---|
| Wrote the CSS and added captions and labels | _Fill in: tested with Tab key only, at phone width, and with a contrast checker_ |

## Technical terms
- **Accessibility**: designing so people with disabilities can use the product.
- **Focus ring**: the outline around the element the keyboard is on.
- **Contrast ratio**: how readable text is against its background. #2C1A0E on #FDF8F3 is about 16:1, well above the WCAG AA minimum of 4.5:1.
- **Responsive**: the layout adapts to the screen size.
- **Media query**: a CSS rule that only applies at certain screen sizes.

## Problem and fix
White text on #E8651A orange is about 3.3:1, below the 4.5:1 needed for normal text. Fix: primary buttons use the dark #2C1A0E text instead, which gives about 5:1. _Verify with a contrast checker and note the result._

## Change from plan
None.

## Screenshots
1. Keyboard focus visible on a button.
2. Dev tools at 375px width.
3. Contrast checker results.
