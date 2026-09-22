# Runway — original AI prompts

Place DESIGN.md beside your project, then choose a task below. These instructions were written for this free collection. Replace sample content with your own requirements.

## 建立新頁面

```text
Read the attached DESIGN.md as the visual reference for a Runway-inspired interface. Implement this working page: A film project gallery with wide visual previews, a quiet editorial introduction, and concise production notes. Avoid autoplay as the only way to understand a project; pair each preview with a useful still image and caption.

Use my product name and content. Prefer existing project components and the current stack. Map the documented colors, typography, spacing, and radii to reusable tokens before styling. Use available system or open fonts when a listed font is unavailable; explain the substitution. 

Make interactive elements work and expose their state to assistive technology. Provide visible keyboard focus, labeled controls, reduced-motion support, and at least 44px touch targets. If an imported visual rule conflicts with usability, make the smallest accessible adjustment and record it. Check the result at 390px, 768px, and 1440px, including long text and empty content. Finish with the implemented files, verification results, and any remaining assumptions.
```

## 製作元件

```text
Read the attached DESIGN.md as the visual reference for a Runway-inspired interface. Build a film project card with duration, format, caption, and play-pause controls. Show it inside a small, realistic example using the existing component conventions. Derive its proportions and visual hierarchy from the reference; do not simply recolor a generic card. Support default, focused, disabled, loading, and error states wherever they apply. Use meaningful sample content and make every visible action functional.

Use my product name and content. Prefer existing project components and the current stack. Map the documented colors, typography, spacing, and radii to reusable tokens before styling. Use available system or open fonts when a listed font is unavailable; explain the substitution. 

Make interactive elements work and expose their state to assistive technology. Provide visible keyboard focus, labeled controls, reduced-motion support, and at least 44px touch targets. If an imported visual rule conflicts with usability, make the smallest accessible adjustment and record it. Check the result at 390px, 768px, and 1440px, including long text and empty content. Finish with the implemented files, verification results, and any remaining assumptions.
```

## 改造既有介面

```text
Read the attached DESIGN.md as the visual reference for a Runway-inspired interface. Restyle the selected page while preserving its routes, data, behavior, and user-facing meaning. First identify the existing page hierarchy and the smallest reusable token and component changes. Use this composition as a visual direction, adapting it to the page rather than adding unrelated features: A film project gallery with wide visual previews, a quiet editorial introduction, and concise production notes. Avoid autoplay as the only way to understand a project; pair each preview with a useful still image and caption.

Use my product name and content. Prefer existing project components and the current stack. Map the documented colors, typography, spacing, and radii to reusable tokens before styling. Use available system or open fonts when a listed font is unavailable; explain the substitution. Apply the visual changes in coherent component groups and check for unintended changes elsewhere. Report the main before-and-after differences.

Make interactive elements work and expose their state to assistive technology. Provide visible keyboard focus, labeled controls, reduced-motion support, and at least 44px touch targets. If an imported visual rule conflicts with usability, make the smallest accessible adjustment and record it. Check the result at 390px, 768px, and 1440px, including long text and empty content. Finish with the implemented files, verification results, and any remaining assumptions.
```

## Iteration workflow

1. Name one observable problem in the current result, such as weak hierarchy or clipped content.
2. Locate the matching token or component rule in DESIGN.md and propose a bounded change.
3. Apply that change without modifying unrelated routes or data behavior.
4. Inspect keyboard focus, narrow-screen layout, and representative content states.
5. Report the result and any deliberate departure from the visual reference.
