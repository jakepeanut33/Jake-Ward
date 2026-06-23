# Western Forms Inc — Website

A modern, single-page marketing site for **Western Forms Inc**, the Kansas City
manufacturer of lightweight aluminum concrete forming systems.

## Highlights

- **Animated "Work" showcase** on the home page — an interactive bento-style
  project grid where cards reveal on scroll, lift and zoom on hover, dim their
  neighbors, and respond to pointer movement with a subtle parallax tilt.
- **Cinematic page-load curtain** and staggered hero text reveals.
- **Scroll-driven reveals**, animated stat counters, parallax backgrounds, an
  infinite marquee, and floating-label contact form.
- Fully responsive with a slide-in mobile menu.
- Respects `prefers-reduced-motion`.
- **Zero dependencies / no build step** — plain HTML, CSS, and vanilla JS.

## Run locally

Just open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Structure

```
index.html        # page markup
css/styles.css    # styles, transitions & animations
js/main.js        # scroll reveals, counters, parallax, nav, form
assets/*.svg      # generated project / about artwork
```

> Imagery is placeholder SVG artwork. Swap the files in `assets/` (or the
> `--img` values in `index.html`) for real project photography when available.
> Contact details are illustrative.
