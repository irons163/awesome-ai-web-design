# Sentry — original AI prompts

Place DESIGN.md beside your project, then choose a task below. These instructions were written for this free collection. Replace sample content with your own requirements.

## 建立新頁面

```text
Read the attached DESIGN.md as the visual reference for a Sentry-inspired interface. Implement this working page: An error triage workspace with an issue list, a stack trace, and release context. Use a deep purple frame and reserve bright accents for severity or selection; keep the trace readable and allow long paths to wrap or scroll.

Use my product name and content. Prefer existing project components and the current stack. Map the documented colors, typography, spacing, and radii to reusable tokens before styling. Use available system or open fonts when a listed font is unavailable; explain the substitution. 

Make interactive elements work and expose their state to assistive technology. Provide visible keyboard focus, labeled controls, reduced-motion support, and at least 44px touch targets. If an imported visual rule conflicts with usability, make the smallest accessible adjustment and record it. Check the result at 390px, 768px, and 1440px, including long text and empty content. Finish with the implemented files, verification results, and any remaining assumptions.
```

## 製作元件

```text
Read the attached DESIGN.md as the visual reference for a Sentry-inspired interface. Build an error summary card with severity, first-seen time, and an acknowledge action. Show it inside a small, realistic example using the existing component conventions. Derive its proportions and visual hierarchy from the reference; do not simply recolor a generic card. Support default, focused, disabled, loading, and error states wherever they apply. Use meaningful sample content and make every visible action functional.

Use my product name and content. Prefer existing project components and the current stack. Map the documented colors, typography, spacing, and radii to reusable tokens before styling. Use available system or open fonts when a listed font is unavailable; explain the substitution. 

Make interactive elements work and expose their state to assistive technology. Provide visible keyboard focus, labeled controls, reduced-motion support, and at least 44px touch targets. If an imported visual rule conflicts with usability, make the smallest accessible adjustment and record it. Check the result at 390px, 768px, and 1440px, including long text and empty content. Finish with the implemented files, verification results, and any remaining assumptions.
```

## 改造既有介面

```text
Read the attached DESIGN.md as the visual reference for a Sentry-inspired interface. Restyle the selected page while preserving its routes, data, behavior, and user-facing meaning. First identify the existing page hierarchy and the smallest reusable token and component changes. Use this composition as a visual direction, adapting it to the page rather than adding unrelated features: An error triage workspace with an issue list, a stack trace, and release context. Use a deep purple frame and reserve bright accents for severity or selection; keep the trace readable and allow long paths to wrap or scroll.

Use my product name and content. Prefer existing project components and the current stack. Map the documented colors, typography, spacing, and radii to reusable tokens before styling. Use available system or open fonts when a listed font is unavailable; explain the substitution. Apply the visual changes in coherent component groups and check for unintended changes elsewhere. Report the main before-and-after differences.

Make interactive elements work and expose their state to assistive technology. Provide visible keyboard focus, labeled controls, reduced-motion support, and at least 44px touch targets. If an imported visual rule conflicts with usability, make the smallest accessible adjustment and record it. Check the result at 390px, 768px, and 1440px, including long text and empty content. Finish with the implemented files, verification results, and any remaining assumptions.
```

## Iteration workflow

1. Name one observable problem in the current result, such as weak hierarchy or clipped content.
2. Locate the matching token or component rule in DESIGN.md and propose a bounded change.
3. Apply that change without modifying unrelated routes or data behavior.
4. Inspect keyboard focus, narrow-screen layout, and representative content states.
5. Report the result and any deliberate departure from the visual reference.
