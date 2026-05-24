---
name: html_description_list_builder
description: |
  Generates semantic, accessible HTML description lists (<dl>) with proper <dt>/<dd> structure, optional <div> grouping, and ARIA labeling.
  TRIGGER: user asks to create a description list, definition list, <dl> element, key-value HTML markup, or asks about dt/dd semantics.
---

# HTML Description List Builder

Build semantic, accessible `<dl>` (description list) markup following modern HTML5 best practices.

## When to use

- "Create a description list for these key-value pairs"
- "How do I use the dl element properly?"
- "Build an accessible definition list in HTML"
- "Generate dt/dd markup for this data"
- "What's the correct way to have multiple values for one term in a dl?"

## How to use

When the user provides key-value or term-description data, generate a `<dl>` following these rules:

### 1. Use `<dt>` for terms and `<dd>` for descriptions

A single `<dt>` can be followed by **multiple** `<dd>` elements when a term has more than one value:

```html
<dl>
  <dt>Author</dt>
  <dd>Jeffrey Zeldman</dd>
  <dd>Ethan Marcotte</dd>
</dl>
```

### 2. Optionally wrap groups in `<div>` for styling

You may wrap each `<dt>`/`<dd>` group in a `<div>` — but **only** a `<div>`, no other element is valid here:

```html
<dl>
  <div>
    <dt>Author</dt>
    <dd>Jeffrey Zeldman</dd>
    <dd>Ethan Marcotte</dd>
  </div>
  <div>
    <dt>Publisher</dt>
    <dd>A Book Apart</dd>
  </div>
</dl>
```

This is useful when you need to apply CSS (e.g., grid or flexbox) to each term-description pair.

### 3. Add ARIA labeling for accessibility

Label the `<dl>` using `aria-labelledby` tied to a nearby heading:

```html
<h2 id="credits">Credits</h2>
<dl aria-labelledby="credits">
  <div>
    <dt>Author</dt>
    <dd>Jeffrey Zeldman</dd>
  </div>
</dl>
```

### 4. Terminology note

Since an HTML5 draft in 2008, `<dl>` stands for **description list**, not "definition list." Use this term in comments and documentation.

### Steps

1. Identify the term-description pairs from the user's data.
2. Determine if any term has multiple descriptions (multiple `<dd>` elements).
3. If the user needs styling hooks or the list is complex, wrap each group in `<div>`.
4. If there is a related heading, add `aria-labelledby` to the `<dl>` for accessibility.
5. Output clean, indented HTML.

## References

- Source article: [On the \<dl\>](https://benmyers.dev/blog/on-the-dl/) via [Simon Willison's Weblog](https://simonwillison.net/2026/May/23/on-the-dl/#atom-everything)
- HTML spec for `<dl>`: [W3C HTML5 — The dl element](https://www.w3.org/TR/2008/WD-html5-20080122/#the-dl)
