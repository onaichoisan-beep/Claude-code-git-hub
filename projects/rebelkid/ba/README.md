# Before/After showcase (measured from the full fraym.fx frame, 720x1280 -> 1080x1920 x1.5)
- Background: per-row colour profiles sampled at x 8-30 and x 692-712 of the reference, blended left->right, fine grain (grad.png).
- Title "The difference editing makes": Raleway 500 49px, ls -0.03em, #F2E2D4, ink top y 288 (NCC 0.85 vs 40 candidates).
- Labels: Raleway 600 italic 46px; "After" #FADFB1 ink right x 931 top 447; "Before" #FFDFB2 ink left x 124 top 558.
- Before panel x 90-484, y 609-1309; After panel x 455-974, y 497-1424 (on top); corner radius 18; soft drop shadow.
- CTA "DM for such UGC Edits": Albert Sans 500 42px, #FFF4D8, ink top y 1569. Handle line (reference: "@fraym.fx", y 1656) left out until the editor's own handle is given.
- Audio: the After edit's mix. Before panel muted.
Build: node layer capture (layer.html #bg / #sh) -> ffmpeg overlay with rounded alpha masks (see conversation command in ba/build.sh).
