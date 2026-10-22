/* Centre lines of every letter in the Caminos del Agua wordmark (logo SVG coordinates).
   Each letter is one continuous pen stroke in handwriting order; drawn with the letter's
   weight it rebuilds the solid shape. `big` is the river: m + S + g in a single line. */
window.LOGO_CENTER = {
  big: {
    w: 17.4,
    // Consecutive strokes, each starting where the last one ends, so the pen never stops.
    // Split only where the logo's weight changes or the pen has to turn back on itself.
    strokes: [
      { w: 17.4, d: 'M421.6 228.4V175.85A43.45 43.45 0 0 1 508.5 175.85V228.4' },                // m: up, first arch, down
      { w: 17.6, d: 'M508.5 228.4V175.85A43.5 43.5 0 0 1 595.5 175.85V219.3' +                   // back up, second arch, down
                    'A30 30 0 0 1 565.5 249.3L443.8 249.4' +                                 // the S
                    'A21.6 21.6 0 0 0 443.8 292.6L486.45 292.6' +
                    'A21.65 21.65 0 0 1 486.45 335.9L412 335.9' +
                    'C398 335.9 389.7 346 389.7 362L389.7 407.5' },                               // down into the g
      { w: 16.9, d: 'M389.7 407.5A42.42 42.42 0 0 0 304.9 407.5A42.42 42.42 0 0 0 389.7 407.5' }, // around the bowl
      { w: 17.0, d: 'M389.7 407.5L389.7 452C389.7 474 375 490 352 493.3C337 495.5 318.75 485.5 313.3 477.1' }, // stem and tail, ending on the logo's angled cut
    ],
  },
  c:   { w: 17.3, strokes: [{ d: 'M276.55 163.45A43.4 43.4 0 1 0 276.55 188.55' }] },
  a1:  { w: 17.5, strokes: [{ d: 'M392.07 123.95V175.85A43.4 43.4 0 0 1 305.26 175.85A43.4 43.4 0 0 1 392.06 175.85' }] },
  i:   { w: 17.8, strokes: [{ d: 'M622 123.58V170C622 192 630 206.5 646.5 215' }] },
  dot: { w: 18.11, strokes: [{ d: 'M621.9 96.4V114.51' }] },
  n:   { w: 16.9, strokes: [{ d: 'M191.09 344.72V291.14A42.24 42.24 0 0 1 275.57 291.14V344.72' }] },
  o:   { w: 17.4, strokes: [{ d: 'M348.27 249.07A43.47 43.47 0 0 0 348.27 336.01A43.47 43.47 0 0 0 348.27 249.07' }] },
  del: { w: 5.4, strokes: [
    { d: 'M579.4 297.69V331.4A10.8 10.8 0 0 1 557 331.4A10.8 10.8 0 0 1 578.6 331.4L579.4 344.13' },   // d
    { d: 'M592.3 334.6L613.2 327.2A10.9 10.9 0 1 0 611 339.1' },                                        // e
    { d: 'M625.9 297.69V344.13' } ] },                                                                   // l
  a3l: { w: 16.9, strokes: [{ d: 'M275.57 357.21V407.54A42 42 0 0 1 191.28 407.54A42 42 0 0 1 275.28 407.54' }] },
  u:   { w: 17.3, strokes: [{ d: 'M421.65 356.91V406.27A43.38 43.38 0 0 0 508.4 406.27V357' }] },
  a3r: { w: 17.2, strokes: [{ d: 'M619.98 357.21V407.55A42.17 42.17 0 0 1 535.64 407.55A42.17 42.17 0 0 1 619.98 407.55' }] },
};
