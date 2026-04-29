# Pencil MCP Tools Guide

## Overview

Pencil exposes design tools via the Model Context Protocol (MCP). The MCP server runs locally and allows AI agents to read, modify, and generate designs in `.pen` files programmatically.

**Critical Rule**: The contents of `.pen` files are encrypted and can only be accessed via Pencil MCP tools. NEVER use `Read`, `Grep`, or `cat` to read `.pen` file contents.

## Tool Reference

### get_editor_state()
**When to use**: At the start of any task to understand the current context.
**Returns**: Active `.pen` file path, current user selection, and other editor state info.

### open_document(filePathOrNew)
**When to use**: When no active editor is open.
- Pass `'new'` to create an empty `.pen` file
- Pass a file path to open an existing `.pen` file

### get_guidelines(topic)
**When to use**: Before designing to get rules and best practices.
**Available topics**: `code`, `table`, `tailwind`, `landing-page`, `slides`, `design-system`, `mobile-app`, `web-app`
**Important**: Only use topics defined above. Do not invent topics.

### get_style_guide_tags
**When to use**: After `get_guidelines` for additional design inspiration.
**Returns**: Available tags to use with `get_style_guide`.

### get_style_guide(tags, name)
**When to use**: When designing screens, websites, apps, or dashboards without an existing design system.
**Parameters**: Relevant tags from `get_style_guide_tags` or a specific style guide name.

### batch_get(patterns, nodeIds)
**When to use**: To discover and understand `.pen` file contents.
**Capabilities**:
- Search for matching patterns in the design tree
- Read specific nodes by ID in batches
- Explore the design hierarchy

### batch_design(operations)
**When to use**: To make design changes — insert, copy, update, replace, move, delete, or generate images.
**Max operations**: Aim for 25 operations per call maximum.

**Operation syntax** (each line is one operation):

```
# Insert a new node under parent
foo=I("parentId", { type: "frame", width: 200, height: 100, fill: "#FF0000" })

# Copy an existing node under a parent with overrides
baz=C("sourceNodeId", "parentId", { fill: "#00FF00" })

# Replace a node (or multiple with /)
foo2=R("nodeId1/nodeId2", { fill: "#0000FF" })

# Update a node (use variable + path)
U(foo+"/childId", { text: "Updated" })

# Delete a node
D("nodeId")

# Move a node to a new parent at index
M("nodeId", "newParentId", 2)

# Generate an AI image on a node
G("nodeId", "ai", "A beautiful sunset over mountains")
```

**Variable references**: Assign results to variables (e.g., `foo=I(...)`) and reference them in subsequent operations (e.g., `U(foo+"/child", {...})`).

### snapshot_layout
**When to use**: To examine computed layout rectangles of each node.
**Purpose**: Understand spatial relationships and decide where to insert new nodes.

### get_screenshot
**When to use**: To validate design visually after making changes.
**Returns**: A rendered screenshot of a node.
**Best practice**: Use periodically to verify changes look correct.

### get_variables / set_variables
**When to use**: To read or modify design tokens (colors, spacing, fonts, etc.).
**Capabilities**: Extract variables, update theme values, sync with CSS.

### find_empty_space_on_canvas
**When to use**: To find available space for placing new design elements.
**Parameters**: Direction and desired size.

### search_all_unique_properties
**When to use**: To audit what property values exist across the design.
**Parameters**: Parent node IDs to search within.

### replace_all_matching_properties
**When to use**: For bulk property changes across the design tree.
**Parameters**: Parent node IDs and property match/replace values.

### export_nodes
**When to use**: To export design elements as images.
**Formats**: PNG, JPEG, WEBP, PDF.

## Built-in Design Libraries

Four pre-configured libraries available:
- **Shadcn UI** — Modern component library
- **Halo** — Design system for UI development
- **Lunaris** — Design library
- **Nitro** — Design framework

Access via the Assets panel in the layers sidebar.

## Built-in Icon Libraries

- Material Symbols (Outlined, Rounded, Sharp)
- Lucide Icons
- Feather
- Phosphor

Import custom SVG icons as standard images.
