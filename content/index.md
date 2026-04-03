# Python Static Site Generator

A from-scratch **Static Site Generator (SSG)** built with Python. This project mimics the core functionality of popular tools like Hugo or Jekyll, transforming Markdown content into a fully functional, SEO-optimized static website.

You can see the generator in action and browse the site it creates here:

## Overview

This generator handles everything from parsing complex Markdown strings to managing recursive directory structures and deploying to GitHub Pages.

**Key Features**

- **Markdown Parsing**: Converts Markdown (including headers, bold, italics, code blocks, links, and images) into a custom HTML Node tree.
- **Recursive Generation**: Automatically mirrors the directory structure of the `/content` folder into the final `/docs` output.
- **Asset Management**: Synchronizes static files (CSS, images) from the `/static` directory.
- **Template Engine**: Injects generated HTML and dynamic titles into a base `template.html`.
- **GitHub Pages Ready**: Includes a configurable `basepath` system to handle subdirectory hosting.

## Project Structure

```
.
├── src/                # Core Python logic
│   ├── main.py         # Application entry point
│   ├── htmlnode.py     # HTML tree structure classes
│   ├── textnode.py     # Markdown-to-Text conversion
│   └── ...             # Logic for blocks, inline styles, etc.
├── content/            # Source Markdown files (.md)
├── static/             # Static assets (CSS, Images)
├── docs/               # Production-ready HTML (Build output)
├── template.html       # Base HTML skeleton
├── build.sh            # Production script: builds for "/repo-name/"
└── main.sh             # Local dev script: builds for "/" and starts a server
```

## How It Works

1. **Clean & Copy**: The script clears the `docs/` folder and copies all assets from `static/`.
2. **Extract & Transform**: It scans the `content/` folder for Markdown files. For each file:
    - Extracts the page title from the first `H1` tag.
    - Parses Markdown into an internal `HTMLNode` tree.
    - Converts the tree into a raw HTML string.
3. **Templating**: It replaces placeholders (`{{ Title }}`, `{{ Content }}`) in the template and fixes URL paths (adding the `basepath`).
4. **Output**: Saves the final `.html` file in the corresponding location within `docs/`.

## Usage

This project separates the local development environment from the production build to ensure links work correctly in both.

### 1. **Local Development (Preview)**

To build the site and spin up a local server to preview your changes:

```
chmod +x main.sh
./main.sh
```

The site will be available at `http://localhost:8888`. This script builds the site with a root basepath (`/`).

### 2. **Production Build (Deploy)**

When you are ready to push to GitHub Pages, run the production build script:

```
chmod +x build.sh
./build.sh
```

This script injects the correct repository name into all internal links (e.g., `/python-static-site-generator/`), ensuring that images and styles load correctly on the live URL.

#### Credits

_This site was generated using a custom Python SSG._

**Author:** Kacper Grzelakowski

[View Source on GitHub](https://github.com/Kacp00rek/python-static-site-generator)
