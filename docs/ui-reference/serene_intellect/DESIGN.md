---
name: Serene Intellect
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#444653'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#757684'
  outline-variant: '#c4c5d5'
  surface-tint: '#3755c3'
  primary: '#00288e'
  on-primary: '#ffffff'
  primary-container: '#1e40af'
  on-primary-container: '#a8b8ff'
  inverse-primary: '#b8c4ff'
  secondary: '#006c4a'
  on-secondary: '#ffffff'
  secondary-container: '#82f5c1'
  on-secondary-container: '#00714e'
  tertiary: '#611e00'
  on-tertiary: '#ffffff'
  tertiary-container: '#872d00'
  on-tertiary-container: '#ffa582'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dde1ff'
  primary-fixed-dim: '#b8c4ff'
  on-primary-fixed: '#001453'
  on-primary-fixed-variant: '#173bab'
  secondary-fixed: '#85f8c4'
  secondary-fixed-dim: '#68dba9'
  on-secondary-fixed: '#002114'
  on-secondary-fixed-variant: '#005137'
  tertiary-fixed: '#ffdbce'
  tertiary-fixed-dim: '#ffb599'
  on-tertiary-fixed: '#370e00'
  on-tertiary-fixed-variant: '#7f2b00'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1'
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.03em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  margin-mobile: 20px
  margin-tablet: 40px
  gutter: 16px
  section-gap: 32px
---

## Brand & Style
This design system is built on the principles of **Mindful EdTech**—a synthesis of high-performance learning tools and meditative clarity. It targets the "lifelong learner" professional who values cognitive ease as much as information retention. 

The aesthetic is **Premium Minimalism** with a **Tactile** twist. While the overall interface remains flat and clean to reduce cognitive load, key learning objects like flashcards and progress modules utilize subtle depth to feel like physical, interactable artifacts. The emotional response is one of calm focus, removing the anxiety often associated with "studying" and replacing it with a sense of curated discovery.

## Colors
The palette is rooted in academic authority and psychological calm. 
- **Deep Blue** is the primary driver for "Action," used for buttons, active states, and navigation. 
- **Emerald Green** represents "Growth" and completion, providing a serotonin hit for finished modules. 
- **Warm Orange** acts as a gentle "Nudge," highlighting items that require review without inducing panic.
- **Surface Strategy:** The UI uses a "White-on-Gray" approach. The true background is the light gray surface, while primary content containers (cards) are pure white, creating a natural hierarchy through contrast rather than heavy lines.

## Typography
The system utilizes **Inter** for its exceptional legibility and neutral, professional tone. 
- **Hierarchy:** We use tight tracking and bold weights for headlines to create a sense of importance. Body text is given a generous line height (1.5-1.6) to prevent eye strain during long reading sessions.
- **Utility:** Small labels and metadata use increased letter-spacing and medium weights to remain legible even at 12px.
- **Mobile Scaling:** For mobile screens, `headline-lg` should scale down to 28px to ensure word-wrap remains clean within 16px margins.

## Layout & Spacing
The layout follows a **Fluid Mobile-First** philosophy with a focus on "Breathable Density."
- **Grid:** A 4-column grid for mobile and 8-column for tablet/desktop. 
- **The 8px Rule:** All margins, paddings, and height increments are multiples of 8px.
- **Safe Zones:** We employ generous horizontal margins (20px on mobile) to ensure content doesn't feel cramped against the device edges.
- **Rhythm:** Use `section-gap` between major card groups and `gutter` between nested elements within a card.

## Elevation & Depth
Elevation in this design system is used sparingly to denote interactivity and "stack order."
- **Level 0 (Floor):** The `#F8FAFC` background.
- **Level 1 (Surface):** Pure white cards with a subtle 2px blur shadow. This is the default for content modules.
- **Level 2 (Flashcard/Active):** A more pronounced shadow (`0 10px 20px rgba(0,0,0,0.04)`) to make learning objects feel like they are floating above the interface, ready to be "picked up" or flipped.
- **Depth via Blur:** Use 4px backdrop blurs for sticky navigation bars to maintain context of the content scrolling beneath them.

## Shapes
The shape language is friendly and approachable without becoming "childish."
- **Standard Radius:** 16px (`rounded-lg`) is the core unit for cards and main UI containers, providing a modern, premium feel.
- **Interactive Elements:** Buttons and input fields use an 8px (`rounded-md`) radius to distinguish them from larger content containers.
- **Status Indicators:** Small chips and badges use a fully rounded "pill" shape.

## Components
- **Flashcards:** The centerpiece. These must be large-format, centered on the screen with `32px` of internal padding. The typography within should be `headline-md`. On tap, they should animate with a 3D flip effect.
- **Primary Buttons:** Solid `#1E40AF` with white text. Height is fixed at `56px` for mobile accessibility (thumb-friendly). No shadows on buttons; use a slight scale-down (0.98) on tap for tactile feedback.
- **Progress Lists:** Clean rows with no borders. Use a `1px` stroke only at the bottom of the row in `#F1F5F9`. Icons are Lucide-style, 24px, with a `1.5pt` stroke weight.
- **Audio Control Bar:** A persistent docked bottom sheet. It uses a semi-transparent white background with a heavy backdrop blur. Controls are fine-line icons.
- **Review Chips:** Small badges used in the "Warning Orange" to indicate how many items are due. These use `label-sm` typography.
- **Input Fields:** Minimalist. A simple `#E2E8F0` border that turns Deep Blue on focus. Labels are positioned above the field in `label-md`.