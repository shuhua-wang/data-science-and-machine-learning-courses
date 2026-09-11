# Course slides (Slidev)

This is a single shared Slidev project for the whole course — one deck per module,
all using the [penguin theme](https://github.com/alvarosabu/slidev-theme-penguin).

| Module                                 | Deck                      |
|----------------------------------------|---------------------------|
| 1 — Environment Setup & Tooling        | `01-environment-setup.md` |
| 2 — Python Programming Basics          | `02-python-basics.md`     |
| 3 — Data Manipulation with pandas      | `03-pandas.md`            |
| 4 — Machine Learning with scikit-learn | `04-scikit-learn.md`      |

## Install

From this `slides/` directory:

```sh
npm install
```

This installs `@slidev/cli`, `@slidev/theme-default` (kept as a fallback theme), and
`slidev-theme-penguin`.

## Preview a deck

Either use one of the npm scripts in `package.json`:

```sh
npm run dev         # previews 01-environment-setup.md by default
npm run dev:03      # previews 03-pandas.md
```

or run Slidev directly against any deck file:

```sh
npx slidev 03-pandas.md
```

This starts a local dev server (default http://localhost:3030) with hot-reload as you
edit the deck.

## Build a deck for sharing

```sh
npx slidev build 03-pandas.md
```

Outputs a static site under `dist/` for that deck. Use `npx slidev export 03-pandas.md`
instead if you want a PDF/PNG export.

## Notes

- `@slidev/theme-default` is listed as a fallback dependency in case the penguin theme
  is unavailable in a given environment; all decks currently set `theme: penguin` in
  their frontmatter.
