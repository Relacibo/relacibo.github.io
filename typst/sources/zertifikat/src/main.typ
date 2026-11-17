// RELACIBO'S KI-BERATUNG — Musterzertifikat (A4 quer)
// Kompilieren (aus Projekt-Root):
// ~/.cargo/bin/typst compile --root typst/sources/zertifikat --font-path typst/sources/zertifikat/fonts typst/sources/zertifikat/src/main.typ public/zertifikat.pdf
#set page(
  width: 29.7cm,
  height: 21cm,
  margin: 1.7cm,
  fill: rgb("#fffdf2"),
)
#set text(font: "Libertinus Serif", size: 11pt, fill: rgb("#1a1a2e"))

#let gold = rgb("#c9a227")
#let muted = rgb("#5a5a72")

// Doppelter Goldrahmen (rein dekorativ, über den Seitenrand gelegt)
#place(rect(width: 100%, height: 100%, stroke: 2.5pt + gold))
#place(rect(width: 100% - 13pt, height: 100% - 13pt, stroke: 0.7pt + gold))

// Diagonaler Muster-Wasserdruck (hinter dem Inhalt)
#place(
  center + horizon,
  rotate(-16deg, text(
    font: "Comic Neue",
    weight: "bold",
    size: 92pt,
    fill: gold.lighten(78%),
    tracking: 0.22em,
  )[MUSTER]),
)

// Regenbogen oben — Pixel-Stretch, wie 1996
#align(center)[#image("/assets/rainbow.png", width: 94%, height: 15pt, fit: "stretch")]

#v(10pt)
#align(center)[
  #text(font: "DejaVu Sans", size: 8.5pt, fill: muted, tracking: 0.16em)[
    RELACIBO'S KI-BERATUNG GMBH & CO. KGAA — ABTEILUNG ZERTIFIZIERUNG
  ]
]

#v(16pt)
#align(center)[
  #text(
    font: "Comic Neue",
    weight: "bold",
    size: 44pt,
    fill: gradient.linear(
      rgb("#ff4d4d"), rgb("#ffb84d"), rgb("#ffff4d"), rgb("#4dff88"),
      rgb("#4dd2ff"), rgb("#d24dff"), rgb("#ff4d4d"),
    ),
  )[ZERTIFIKAT]
]
#v(4pt)
#align(center)[
  #text(size: 10.5pt, tracking: 0.1em)[
    #emph[über die erfolgreiche Teilnahme an der #strong[63-Tage-Methode™]]
  ]
]

#v(1fr)

#align(center)[
  #text(size: 12pt)[Hiermit wird bestätigt, dass]
]
#v(10pt)
#align(center)[
  #underline(
    stroke: (paint: gold, thickness: 0.8pt, dash: "dotted"),
    extent: 14pt,
  )[
    #text(font: "Comic Neue", weight: "bold", size: 25pt)[Max Mustermann]
  ]
]
#v(10pt)
#align(center)[
  #text(size: 12pt)[
    die #strong[63-Tage-Methode™] in vollem Umfang absolviert und fortan den Status
    eines #strong[zertifizierten KI-Beraters] innehat.
  ]
]

#v(1fr)

#align(center)[
  #text(size: 9.5pt, fill: muted)[
    Zertifikat-Nr. KI-1996-063 · Ausgestellt am 17.11.2026 · Gültigkeit: unbefristet
  ]
]

#v(1fr)

// Unterschrift & Siegel
#grid(
  columns: (1fr, 3cm),
  align: (left + bottom, center + bottom),
  [
    #text(font: "Comic Neue", style: "italic", weight: "bold", size: 21pt, fill: rgb("#0d3b66"))[Relacibo]
    #v(2pt)
    #line(length: 58%, stroke: 0.6pt + rgb("#1a1a2e"))
    #text(size: 8.5pt, fill: muted)[Gründer & Zertifizierungsstelle]
  ],
  rotate(-6deg, image("/assets/seal.png", width: 2.2cm)),
)

#v(8pt)
#align(center)[#image("/assets/rainbow.png", width: 88%, height: 14pt, fit: "stretch")]
#v(5pt)
#align(center)[
  #text(font: "DejaVu Sans", size: 7pt, fill: muted)[
    Optimiert für Papier (A4 quer) · 100% druckkompatibel · Y2K-fest · Erstellt mit AI: GLM-5.3-Flash
  ]
]
#v(14pt)
