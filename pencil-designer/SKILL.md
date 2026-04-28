---
name: pencil-designer
description: This skill should be used when working with Pencil design files (.pen), creating or editing designs in the Pencil editor, using Pencil MCP tools, building UI layouts, managing design systems/libraries, or generating code from Pencil designs. Triggers on "pencil", ".pen file", "design in pencil", "create a design", "design library", "pen file", or when Pencil MCP tools are available and design work is requested.
---

# Pencil Designer

This skill provides comprehensive guidance for working with Pencil -- a vector design tool that integrates directly into development environments. Pencil bridges design and development by operating within IDEs, enabling designers and developers to collaborate using familiar version control workflows.

## When to Use This Skill

- Creating or editing designs in `.pen` files
- Working with Pencil MCP tools (batch_design, batch_get, etc.)
- Building UI layouts, screens, dashboards, or components
- Managing design libraries and design systems
- Generating code from Pencil designs or importing code into designs
- Working with design variables and theming
- Creating reusable components with slots

## Critical Rules

1. **NEVER use Read, Grep, or cat to read `.pen` files** -- contents are encrypted and only accessible via Pencil MCP tools
2. **Always start with `get_editor_state()`** to understand the current context before making changes
3. **Use `get_screenshot`** periodically to validate design changes visually
4. **Limit `batch_design` to ~25 operations per call** to avoid overwhelming the system

## Workflow

### Starting a Design Task

1. Call `get_editor_state()` to check the active `.pen` file and current selection
2. If no file is open, call `open_document('new')` for a new file or `open_document(path)` for existing
3. Call `get_guidelines(topic)` for relevant design rules (topics: `code`, `table`, `tailwind`, `landing-page`, `slides`, `design-system`, `mobile-app`, `web-app`)
4. Call `get_style_guide_tags` then `get_style_guide(tags)` for design inspiration when not using an existing design system
5. Use `snapshot_layout` to understand existing layout structure before inserting

### Making Design Changes

Use `batch_design(operations)` with this operation syntax:

```
# Insert new node
varName=I("parentId", { type: "frame", width: 200, height: 100, fill: "#FF0000" })

# Copy existing node
copy=C("sourceId", "parentId", { fill: "#00FF00" })

# Replace node(s)
R("nodeId1/nodeId2", { fill: "#0000FF" })

# Update node (reference variables from prior operations)
U(varName+"/childId", { text: "Updated text" })

# Delete node
D("nodeId")

# Move node to new parent at index
M("nodeId", "newParentId", 2)

# Generate AI image
G("nodeId", "ai", "A sunset over mountains")
```

### Discovering Content

- Use `batch_get(patterns)` to search for nodes by pattern
- Use `batch_get(nodeIds)` to read specific nodes by ID
- Use `search_all_unique_properties` to audit property values across the tree
- Use `snapshot_layout` to see computed layout rectangles

### Validating Changes

After making changes, call `get_screenshot` to render a visual preview. Verify:
- Layout looks correct (alignment, spacing)
- Colors and typography match intent
- Components render properly
- No overlapping or misaligned elements

## Node Types

| Type | Purpose |
|------|---------|
| `frame` | Main container with children and layout (flexbox-like) |
| `rectangle` | Basic rectangle shape |
| `ellipse` | Circle/ellipse |
| `text` | Text element |
| `line` | Line element |
| `polygon` | Multi-sided polygon |
| `path` | SVG-like path |
| `group` | Unstyled grouping container |
| `ref` | Instance of a reusable component |
| `icon_font` | Icon from built-in font libraries |

## Layout Properties

Frames support flexbox-like layout:

| Property | Values |
|----------|--------|
| `layout` | `"none"`, `"vertical"`, `"horizontal"` |
| `gap` | number (space between children) |
| `padding` | number or `{top, right, bottom, left}` |
| `justifyContent` | `"start"`, `"center"`, `"end"`, `"space_between"`, `"space_around"` |
| `alignItems` | `"start"`, `"center"`, `"end"` |

Child sizing: use fixed `width`/`height` or `"fit_content"` / `"fill_container"`.

## Styling Properties

### Fill
- Solid: `{ fill: "#3B82F6" }` or `{ fill: { type: "solid", color: "#3B82F6" } }`
- Gradient: `{ fill: { type: "linear_gradient", stops: [...], angle: 0 } }`
- Image: `{ fill: { type: "image", url: "..." } }`

### Stroke
```json
{ "stroke": { "fill": "#000", "thickness": 1, "alignment": "inside" } }
```

### Effects
```json
{ "effect": [{ "type": "shadow", "x": 0, "y": 4, "blur": 8, "color": "#00000020" }] }
```

### Text
Key properties: `fontSize`, `fontFamily`, `fontWeight`, `fontStyle`, `letterSpacing`, `lineHeight`, `textAlign` ("left"/"center"/"right"/"justify"), `textAlignVertical` ("top"/"middle"/"bottom"), `textGrowth` ("auto"/"fixed-width"/"fixed-width-height").

### Other
- `opacity`: 0-1
- `cornerRadius`: number or per-corner object
- `rotation`: degrees (counter-clockwise)
- `enabled`: boolean (visibility)

## Components

### Creating Components
Set `reusable: true` on any node to make it a component origin (magenta bounding box).

### Creating Instances
Use `ref` type: `{ type: "ref", ref: "componentId", descendants: { "childId": { overrides } } }`

### Slots
Frames marked with `slot` property become designated drop zones within components. Only empty frames in component origins can be slots.

## Variables and Theming

### Defining Variables
Variables act as design tokens -- define once, reference everywhere with `$variable-name` syntax.

Types: `color`, `number`, `string`, `boolean`

### Theme Support
Variables can have theme-conditional values for light/dark mode or other theme axes.

### Managing Variables
- `get_variables` -- read current tokens and themes
- `set_variables` -- add or update variables
- AI can import variables from CSS (`globals.css`) or Figma

## Design Libraries

### Built-in Libraries
- **Shadcn UI** -- Modern component library
- **Halo** -- UI design system
- **Lunaris** -- Design library
- **Nitro** -- Design framework

### Custom Libraries
1. Create a `.pen` file with components
2. Turn it into a library (creates `.lib.pen` suffix -- irreversible)
3. Import into other `.pen` files via the Libraries panel

### Built-in Icon Libraries
Material Symbols (Outlined/Rounded/Sharp), Lucide Icons, Feather, Phosphor

## Design-to-Code / Code-to-Design

### Design to Code
Select elements, open AI chat (Cmd/Ctrl+K), and request code generation. Supports React, Vue, Next.js, Svelte, Tailwind CSS, CSS Modules, and any framework.

### Code to Design
Keep `.pen` file in the same workspace as code. AI can recreate code components as Pencil designs.

### Variable Sync
Synchronize design variables between Pencil and CSS files bidirectionally.

## Import/Export

### Import
- **Figma**: Full files via toolbar import or individual layers via copy/paste (images must be imported separately)
- **Images**: Drag-and-drop, clipboard paste, or toolbar import (PNG, JPEG, SVG)
- **Icons**: Built-in libraries or custom SVG

### Export
- Elements as PNG, JPEG, WEBP, or PDF via properties panel
- Code generation via AI chat

## Best Practices

1. **Save frequently** -- no auto-save yet (Cmd/Ctrl+S)
2. **Commit `.pen` files to Git** -- they are version-control friendly and diff cleanly, but always use MCP tools to read or edit their contents
3. **Use variables** instead of hardcoded values for colors, spacing, and fonts
4. **Create components** for repeated UI elements to maintain consistency
5. **Use descriptive names** for layers and components (e.g., `dashboard-header`, `user-card`)
6. **Validate visually** with `get_screenshot` after batch operations
7. **Use `snapshot_layout`** before inserting to understand spatial relationships
8. **Iterate progressively** -- start broad, then refine details
9. **Use style guides** via `get_style_guide` when not working with an existing design system
