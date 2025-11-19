# Installing Graphviz for PNG Export

## Current Status

✅ **Good news!** Your script works without `pygraphviz`!

LangGraph's `draw_mermaid_png()` method can work without `pygraphviz` in many cases. The Mermaid text format always works and is great for documentation.

## If You Want to Install pygraphviz (Optional)

If you encounter issues with PNG export or want additional graphviz features, you can install `pygraphviz`:

### Prerequisites

1. **System graphviz is already installed** ✅
   ```bash
   dot -V  # Should show version
   ```

2. **Install pygraphviz** (optional):
   ```bash
   uv pip install pygraphviz
   ```

   If this fails, you may need graphviz development headers:
   ```bash
   # macOS
   brew install graphviz
   
   # Linux
   sudo apt-get install graphviz graphviz-dev
   ```

## What Works Without pygraphviz

- ✅ Mermaid text diagrams (always works)
- ✅ PNG export (works in most cases via LangGraph's built-in method)
- ✅ Saving Mermaid to `.mmd` files

## What Requires pygraphviz

- Advanced graphviz features
- Custom graph layouts
- Some edge cases in PNG generation

## Recommendation

**You don't need to install pygraphviz** unless you encounter specific issues. The current setup works great!

If you do want to install it later:
```bash
uv pip install pygraphviz
```

