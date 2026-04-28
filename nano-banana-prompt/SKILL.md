---
name: nano-banana-prompt
description: This skill should be used when users need to create detailed, effective prompts for Gemini Nano Banana (or Nano Banana Pro) image generation. Use when users ask for "image prompts", "create a prompt for", "visualize this scene", "generate art of", or need help crafting prompts for AI image generation. Ideal for book illustrations, concept art, character designs, scene visualization, and creative projects requiring precise visual output.
---

# Nano Banana Prompt Generator

## Overview

Nano Banana is Google's autoregressive image generation model (also known as Gemini 2.5 Flash Image, and the Pro version as Gemini 3 Pro Image). This skill generates optimized prompts that leverage Nano Banana's unique capabilities: strong prompt adherence, character consistency, and nuanced control through structured formatting.

## Core Prompting Formula

Every Nano Banana prompt follows this structure:

**Subject + Action + Environment + Art Style + Lighting + Details**

| Component | Description | Example |
|-----------|-------------|---------|
| Subject | Main character or object | "A three-meter tall corrupted construct" |
| Action | What the subject is doing | "stalking through ruins" |
| Environment | Location/background | "ancient forge facility" |
| Art Style | Visual aesthetic | "dark fantasy concept art" |
| Lighting | Light sources and quality | "bioluminescent inner glow" |
| Details | Specific requirements | "crystalline growths, pulsing core" |

## Key Techniques

### 1. Use Markdown Formatting

Structure prompts with headers, bullet points, and sections. Nano Banana's text encoder parses markdown effectively.

```markdown
# Subject
[Main focus description]

## Core Design
- Detail 1
- Detail 2

## Environment
[Background/setting]
```

### 2. Capitalize Enforcement Keywords

Use ALL CAPS for critical requirements:
- **MUST** - Mandatory elements
- **DO NOT** - Forbidden elements
- **ONLY** - Exclusive requirements

Example: "The composition MUST use portrait orientation"

### 3. Specify Technical Parameters

Include camera and composition specifications:

| Parameter | Options |
|-----------|---------|
| Aspect Ratio | 16:9, 9:16, 1:1, 4:3, 3:2 |
| Camera | Canon EOS 90D, 24mm wide angle, 85mm portrait |
| Composition | Rule of thirds, golden ratio, centered |
| Perspective | Eye level, low angle, bird's eye, Dutch angle |
| Depth of Field | Shallow, deep, selective focus |

### 4. Layer Lighting Sources

Specify multiple light sources for depth:

```markdown
## Lighting
- Primary: [Main light source and direction]
- Secondary: [Fill light or ambient]
- Accent: [Rim light, highlights, glows]
```

### 5. Use Prestige Anchoring

Reference acclaimed artists or prestigious descriptors to improve quality:

| Category | Effective Anchors |
|----------|-------------------|
| Dark Fantasy | "Beksinski meets industrial horror" |
| Illustration | "Bernie Wrightson, Gustave Doré" |
| Photo Quality | "Pulitzer Prize winning photograph" |
| Concept Art | "Art station trending, Weta Workshop" |
| Portrait | "Annie Leibovitz lighting" |

### 6. Include Negative Constraints

Always add a "Do NOT Include" section:

```markdown
## Do NOT Include
- Text, watermarks, or logos
- Modern anachronistic elements
- [Style-specific exclusions]
```

## Prompt Template

Use this template structure for all Nano Banana prompts:

```markdown
# [Title/Subject Name]

## Format Specifications
- **Orientation**: [Portrait/Landscape/Square] ([aspect ratio])
- **Color**: [Full color / Black and white / Limited palette]
- **Purpose**: [Book illustration / Concept art / Character design]

## Subject
[Detailed description of the main focus]

## Core Design
- [Key visual element 1]
- [Key visual element 2]
- [Key visual element 3]

## Critical Details (MUST include)
- [Non-negotiable element 1]
- [Non-negotiable element 2]

## Environment
[Setting, background, atmospheric details]

## Art Style
[Specific aesthetic, artist references, medium]

## Lighting
- Primary: [Main light]
- Secondary: [Fill/ambient]
- Accent: [Highlights/glows]

## Composition
[Rule of thirds, framing, focal points, camera specs]

## Atmosphere/Mood
[Emotional tone, narrative context]

## Technical Specifications
[Print quality, detail density, rendering style]

## Do NOT Include
- [Exclusion 1]
- [Exclusion 2]
- [Exclusion 3]
```

## Workflow

### Step 1: Gather Parameters

Collect from user or determine from context:

| Parameter | Question |
|-----------|----------|
| Subject | What is the main focus of the image? |
| Purpose | Book illustration, concept art, character sheet, scene? |
| Style | Realistic, stylized, illustrated, photographic? |
| Format | Portrait, landscape, square? Color or B&W? |
| Mood | What emotion or atmosphere? |
| References | Any existing art style or artist to match? |

### Step 2: Analyze Source Material

When generating prompts from written descriptions (scenes, chapters, etc.):

1. Identify the most visually dynamic moment
2. Extract specific physical details (colors, materials, scale)
3. Note environmental context
4. Capture emotional/atmospheric tone
5. Identify any unique or fantastical elements requiring special attention

### Step 3: Structure the Prompt

Build the prompt using the template, ensuring:

1. **Subject section** clearly establishes the main focus
2. **Core Design** breaks down visual components systematically
3. **MUST/DO NOT** sections enforce critical requirements
4. **Art Style** anchors to recognizable aesthetics
5. **Lighting** creates depth with multiple sources
6. **Composition** specifies camera and framing

### Step 4: Validate and Refine

Check the prompt against these criteria:

| Criterion | Check |
|-----------|-------|
| Specificity | Are measurements, colors, materials explicit? |
| Enforcement | Are critical elements marked with MUST/ONLY? |
| Exclusions | Is there a DO NOT section? |
| Style Anchor | Is there a prestige reference? |
| Technical Specs | Are format, camera, lighting specified? |
| Clarity | Could another AI parse this unambiguously? |

## Special Formats

### Black and White Illustration

Add these specifications:
```markdown
## Format Specifications
- **Color**: BLACK AND WHITE ONLY—high contrast monochromatic, no color

## Art Style
- High contrast black and white ink illustration
- Style: [Artist reference] (e.g., Bernie Wrightson, Frank Miller)
- Heavy blacks for shadows
- Pure whites for highlights
- Crosshatching for texture and gradation
```

### Character Design Sheet

Add these specifications:
```markdown
## Format Specifications
- **Purpose**: Character design reference sheet
- **Views**: Front, 3/4, profile (or specify which)

## Character Details
- Height/build reference
- Distinctive features
- Costume/clothing breakdown
- Color callouts (if color)
- Expression range (if multiple expressions)
```

### Action Scenes

Add motion indicators:
```markdown
## Motion and Energy
- Speed lines style: [Classic illustration / manga / subtle blur]
- Motion direction: [Left-to-right / diagonal / toward camera]
- Dynamic elements: [Hair, clothing, debris, particles]
- Frozen moment: [Describe the exact instant captured]
```

## Quality Standards

Every generated prompt must:

1. **Use Markdown Structure** - Headers, bullets, clear sections
2. **Include Format Specs** - Orientation, color mode, purpose
3. **Specify Subject Clearly** - Main focus with physical details
4. **Enforce Critical Elements** - MUST/DO NOT sections present
5. **Anchor Style** - Artist reference or prestige descriptor
6. **Layer Lighting** - At least 2 light sources described
7. **Define Composition** - Camera, framing, focal point
8. **Exclude Unwanted Elements** - Clear DO NOT section

## Example Usage

User: "Create a prompt for a dragon attacking a castle at sunset"

Response approach:
1. Determine format (likely landscape for epic scene)
2. Establish subject (dragon as focus, castle as environment)
3. Select style anchors (fantasy art references)
4. Specify dramatic sunset lighting (golden hour + fire)
5. Add motion for attack (wings, fire breath, debris)
6. Exclude common unwanted elements (text, watermarks)
7. Structure using full template

## References

For additional guidance on Nano Banana capabilities, consult:
- [Max Woolf's Nano Banana Prompting Guide](https://minimaxir.com/2025/11/nano-banana-prompts/)
- [Google's Nano Banana Pro Prompting Tips](https://blog.google/products/gemini/prompting-tips-nano-banana-pro/)

## Editing Images (Nano Banana Pro)

When editing existing images rather than generating new ones, use these five action words:

| Action | Use Case | Example |
|--------|----------|---------|
| **Add** | Insert new elements | "Add a dragon flying in the background" |
| **Change** | Modify existing elements | "Change the sky to sunset colors" |
| **Make** | Transform qualities | "Make the character look older" |
| **Remove** | Delete elements | "Remove the text in the corner" |
| **Replace** | Substitute elements | "Replace the sword with an axe" |
