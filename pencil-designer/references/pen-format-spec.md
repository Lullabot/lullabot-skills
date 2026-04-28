# The .pen Format Specification

## Core Structure

> **Note:** This specification describes the logical document structure exposed by Pencil's MCP tools. On disk, `.pen` file contents are encrypted and must only be accessed via MCP -- never with `Read`, `Grep`, or `cat`.

The .pen format stores design documents as JSON describing an object tree. Each object requires:
- **id**: Unique string identifier (no forward slashes allowed)
- **type**: Object type from supported set
- **x, y**: Position coordinates on infinite 2D canvas
- **name** (optional): Display name
- **context** (optional): Context information

## Document Root Properties

```json
{
  "version": "2.9",
  "themes": {},
  "imports": [],
  "variables": [],
  "children": []
}
```

- **version**: Format version
- **themes**: Theme axis definitions (e.g., light/dark mode)
- **imports**: References to external .pen files (design libraries)
- **variables**: Document-wide design tokens
- **children**: Array of top-level objects

## Supported Object Types

### Shapes
- `rectangle` - Basic rectangle shape
- `ellipse` - Circle/ellipse shape
- `line` - Line element
- `polygon` - Multi-sided polygon
- `path` - SVG-like path

### Containers
- `frame` - Main container, can have children and layout (flexbox-like)
- `group` - Unstyled container for grouping

### Content
- `text` - Text element
- `note` - Annotation note
- `prompt` - AI prompt element
- `context` - Context information element
- `icon_font` - Icon from font libraries

### Special
- `ref` - Instance of a reusable component

## Layout System

Parent objects control child sizing/positioning via flexbox-style properties:

| Property | Values | Description |
|----------|--------|-------------|
| `layout` | `"none"`, `"vertical"`, `"horizontal"` | Layout direction |
| `gap` | number | Space between children |
| `padding` | number or `{top, right, bottom, left}` | Inside edge spacing |
| `justifyContent` | `"start"`, `"center"`, `"end"`, `"space_between"`, `"space_around"` | Main axis alignment |
| `alignItems` | `"start"`, `"center"`, `"end"` | Cross axis alignment |

### Child Sizing

Children can have fixed `width`/`height` or use **SizingBehavior** values:
- `"fit_content"` - Size to content
- `"fill_container"` - Fill available space in parent

## Graphics Properties

### Fill
Supports multiple fill types:
- **Solid color**: `{"type": "solid", "color": "#RRGGBB"}` or with alpha `"#RRGGBBAA"`
- **Linear gradient**: `{"type": "linear_gradient", "stops": [...], "angle": 0}`
- **Radial gradient**: `{"type": "radial_gradient", "stops": [...]}`
- **Angular gradient**: `{"type": "angular_gradient", "stops": [...]}`
- **Image**: `{"type": "image", "url": "..."}`
- **Mesh gradient**: `{"type": "mesh_gradient", ...}`

### Stroke
Single stroke with configurable properties:
- `fill`: Same fill options as above
- `alignment`: inside, center, outside
- `thickness`: number
- `join`: miter, round, bevel
- `cap`: butt, round, square
- `dash`: dash pattern array

### Effects
Multiple effects applied sequentially:
- `blur` - Gaussian blur
- `background_blur` - Backdrop blur
- `shadow` - Drop shadow with x, y, blur, spread, color

### Other Visual Properties
- `opacity`: 0-1 range
- `rotation`: Counter-clockwise degrees
- `blendMode`: normal, darken, multiply, screen, overlay, etc. (15+ modes)
- `flipX`, `flipY`: Boolean transformations
- `cornerRadius`: Border radius (number or per-corner object)

## Text Properties

| Property | Values | Description |
|----------|--------|-------------|
| `fontSize` | number | Font size |
| `fontFamily` | string | Font name |
| `fontWeight` | number/string | Weight (400, 700, "bold", etc.) |
| `fontStyle` | `"normal"`, `"italic"` | Font style |
| `letterSpacing` | number | Character spacing |
| `lineHeight` | number | Line height |
| `textAlign` | `"left"`, `"center"`, `"right"`, `"justify"` | Horizontal alignment |
| `textAlignVertical` | `"top"`, `"middle"`, `"bottom"` | Vertical alignment |
| `underline` | boolean | Underline decoration |
| `strikethrough` | boolean | Strikethrough decoration |
| `href` | string | Link URL |
| `textGrowth` | `"auto"`, `"fixed-width"`, `"fixed-width-height"` | Text box sizing |

## Components and Instances

### Creating Components
Set `reusable: true` on any object to make it a component (origin). The origin has a magenta bounding box.

### Creating Instances
Use the `ref` type to create instances:
```json
{
  "type": "ref",
  "ref": "component-id",
  "descendants": {
    "child-id": { "property": "override-value" }
  }
}
```

**Descendants** support:
- Property overrides (excluding id, type, children)
- Complete object replacement (when type is present)
- Children replacement for container/slot patterns
- Path syntax: `"parent/child"` for nested customization

## Slots

Frames marked with the `slot` property (array of component IDs) indicate designated drop zones within components. Slots:
- Display diagonal line patterns on canvas
- Only empty frames within component origins can become slots
- Can have "suggested slot components" to guide content placement

## Variables and Theming

### Variable Types
- `boolean`
- `color` (HEX codes)
- `number` (spacing, border radii, sizes)
- `string` (font names)

### Single Value
```json
{ "name": "primary", "type": "color", "value": "#3B82F6" }
```

### Theme-Conditional Values
```json
{
  "name": "background",
  "type": "color",
  "value": [
    { "value": "#FFFFFF", "theme": { "mode": "light" } },
    { "value": "#1A1A1A", "theme": { "mode": "dark" } }
  ]
}
```

### Theme Definitions
```json
{
  "themes": {
    "mode": ["light", "dark"]
  }
}
```
First value in each axis is the default.

### Referencing Variables
Use `$variable-name` syntax in property values.

## Additional Properties

- `enabled`: Boolean or variable reference -- controls visibility
- `layoutPosition`: `"auto"` (flow) or `"absolute"` (positioned)
- `metadata`: Custom type information for the node
