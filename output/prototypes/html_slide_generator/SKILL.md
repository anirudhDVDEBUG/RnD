---
name: HTML Slide Generator
description: |
  Generate professional HTML slide presentations from text content, outlines, or topics.
  TRIGGER: user asks to create slides, make a presentation, generate a deck, build an HTML slideshow, convert notes to slides, or create a pitch deck.
---

# HTML Slide Generator

Create stunning, self-contained HTML slide presentations that work in any modern browser with no external dependencies.

## When to use

- "Create a presentation about [topic]"
- "Turn these notes into slides"
- "Generate an HTML slide deck for my talk"
- "Make a pitch deck for [product/idea]"
- "Build a slideshow from this outline"

## How to use

1. **Gather content**: Identify the topic, key points, or outline the user wants presented. Ask clarifying questions if the scope is unclear (number of slides, audience, tone).

2. **Choose a layout style**: Select from common slide patterns:
   - **Title slide**: Large heading + subtitle/author
   - **Content slide**: Heading + bullet points or short paragraphs
   - **Image slide**: Full-bleed background or side-by-side with text
   - **Two-column slide**: Compare/contrast or text + visual
   - **Quote slide**: Large quotation with attribution
   - **Code slide**: Syntax-highlighted code block
   - **Closing/CTA slide**: Summary or call-to-action

3. **Generate a single HTML file** with these characteristics:
   - Self-contained (inline CSS, no external dependencies)
   - Keyboard navigation (Arrow keys, Space, Enter to advance; Backspace/Left to go back)
   - Responsive design that scales to any viewport
   - Print-friendly with `@media print` styles
   - Clean typography using system font stacks
   - Smooth slide transitions (CSS transforms)
   - Slide counter/progress indicator
   - Touch/swipe support for mobile

4. **Structural template**:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>[Presentation Title]</title>
     <style>
       *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
       html, body { height: 100%; overflow: hidden; font-family: system-ui, -apple-system, sans-serif; }
       .deck { height: 100vh; position: relative; }
       .slide { position: absolute; inset: 0; display: flex; flex-direction: column;
                justify-content: center; align-items: center; padding: 4rem;
                opacity: 0; transition: opacity 0.4s ease; pointer-events: none; }
       .slide.active { opacity: 1; pointer-events: auto; }
       h1 { font-size: clamp(2rem, 5vw, 4rem); font-weight: 700; margin-bottom: 1rem; }
       h2 { font-size: clamp(1.5rem, 3.5vw, 2.5rem); font-weight: 600; margin-bottom: 0.75rem; }
       p, li { font-size: clamp(1rem, 2vw, 1.5rem); line-height: 1.6; }
       ul { text-align: left; max-width: 70%; }
       .progress { position: fixed; bottom: 0; left: 0; height: 4px;
                   background: #2563eb; transition: width 0.3s ease; }
       .counter { position: fixed; bottom: 1rem; right: 1rem;
                  font-size: 0.875rem; color: #64748b; }
     </style>
   </head>
   <body>
     <div class="deck">
       <div class="slide active">
         <h1>[Title]</h1>
         <p>[Subtitle or Author]</p>
       </div>
       <div class="slide">
         <h2>[Heading]</h2>
         <ul><li>[Point]</li></ul>
       </div>
     </div>
     <div class="progress" id="progress"></div>
     <div class="counter" id="counter"></div>
     <script>
       const slides = document.querySelectorAll('.slide');
       let current = 0;
       function goTo(n) {
         slides[current].classList.remove('active');
         current = Math.max(0, Math.min(n, slides.length - 1));
         slides[current].classList.add('active');
         document.getElementById('progress').style.width =
           ((current + 1) / slides.length * 100) + '%';
         document.getElementById('counter').textContent =
           (current + 1) + ' / ' + slides.length;
       }
       document.addEventListener('keydown', e => {
         if (['ArrowRight','Space','Enter'].includes(e.key)) goTo(current + 1);
         if (['ArrowLeft','Backspace'].includes(e.key)) goTo(current - 1);
       });
       let touchStartX = 0;
       document.addEventListener('touchstart', e => touchStartX = e.touches[0].clientX);
       document.addEventListener('touchend', e => {
         const diff = touchStartX - e.changedTouches[0].clientX;
         if (Math.abs(diff) > 50) goTo(current + (diff > 0 ? 1 : -1));
       });
       goTo(0);
     </script>
   </body>
   </html>
   ```

5. **Design best practices**:
   - Limit text to 6 lines per slide maximum
   - Use high-contrast color schemes (dark on light or light on dark)
   - One idea per slide
   - Use visual hierarchy: size, weight, color to guide attention
   - Add subtle gradients or accent colors for visual interest
   - Aim for 10-20 slides for a standard presentation

6. **Save the file** as `[topic-slug]-slides.html` in the current directory or as specified by the user.

## References

- Source: [ToseaAI/awesome-html-slide-skills](https://github.com/ToseaAI/awesome-html-slide-skills)
