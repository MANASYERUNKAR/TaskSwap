# TaskSwap Design Exploration

## Approach 1 — Quiet Utility
**Very Brief Intro:** A disciplined, near-monochrome product experience informed by Apple’s product pages. It lets task titles, actions, and generous empty space do the visual work.

**Probability:** 0.07

## Approach 2 — Civic Bulletin
**Very Brief Intro:** A sturdy public-service interface with crisp typographic hierarchy and indexed information. It would foreground locality and practical exchange over product theater.

**Probability:** 0.04

## Approach 3 — Night Shift Exchange
**Very Brief Intro:** A near-black, late-night task board with a single electric signal color and high-contrast editorial type. It would feel focused and slightly more energetic.

**Probability:** 0.09

---

# Chosen Direction — Quiet Utility

## Design Movement
**Apple product-page minimalism**, translated into a practical local marketplace: technical restraint, cinematic whitespace, confident sans-serif type, and one intentional blue interaction color.

## Core Principles
1. **One idea per plane:** Every major section presents a single statement or action without competing visual decoration.
2. **Typography is the interface:** Large display headlines, clear metadata, and exact spacing carry hierarchy in place of imagery.
3. **Calm friction reduction:** Primary decisions have obvious high-contrast paths; secondary details remain quiet but readable.
4. **Precision in state:** Status, availability, empty states, and permissions are explicit rather than implied.

## Color Philosophy
The default surface is a warm, nearly-white porcelain that makes the interface feel physical but clean. Ink-black is reserved for structural type and primary controls. **TaskSwap Blue (#0071E3)** is the sole signal color, used only for links, key calls-to-action, and focus treatment so important interaction always reads instantly.

## Layout Paradigm
The homepage uses a **sequence of full-height typographic stages**, not a card-filled centered grid: an introductory stage, three declarative exchange stages, then a quieter task shelf. Application, account, moderation, and task pages use a contained workbench with an asymmetric information/action rhythm.

## Signature Elements
1. **Black pill controls** with precise blue text-link alternatives.
2. **Hairline dividers and oversized display statements** as section boundaries.
3. **Monogram-style “TS” mark** built from a compact black square and white letterform rather than a generic icon.

## Interaction Philosophy
Controls acknowledge intent through brief opacity and scale transitions. Status actions require explicit labeled forms, and authentication feedback is direct and non-revealing. No decorative motion competes with completing a task.

## Animation
Sections begin 22px lower at 0% opacity and arrive through a 720ms `cubic-bezier(0.22, 1, 0.36, 1)` reveal when they enter the viewport. Hover and focus transitions stay within 160–220ms. `prefers-reduced-motion` removes all nonessential movement.

## Typography System
Use the platform stack: `-apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Arial, sans-serif`. Display headlines use 700–800 weight, tight negative tracking, and 56–116px responsive sizing. Interface text uses 400–600 weight at compact, readable scales; metadata remains smaller and muted, never faint.

## Brand Essence
**TaskSwap is the clear, local place for turning a small need into a completed task, for people who value practical help without marketplace noise.**

Personality: **clear, capable, neighborly**.

## Brand Voice
Headlines are brief and declarative. CTAs state the action, while microcopy tells the user what will happen next in plain language.

Examples: “**Put the ask out there.**” and “**One clear task. One real hand.**”

## Wordmark & Logo
Use a compact black rounded-square monogram with the white letters **TS**, paired with a bold, tightly tracked TaskSwap wordmark. This is a simple ownable mark built from the product’s name, not a stock or library icon.

## Signature Brand Color
**TaskSwap Blue — #0071E3**

## Style Decisions
- Avoid imagery, gradients, fake testimonials, icon libraries, ornamental shadows, and generic product-dashboard decoration.
- Keep every template in the porcelain/ink/blue system with distinctive oversized type and pill controls.
- Let task data and visible status communicate utility; do not simulate activity or social proof.
