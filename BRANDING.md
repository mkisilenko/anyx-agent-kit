# Anyx branding

**TLDR:** Use the supplied original PNG unchanged. The three visual skills carry their own identical copy and embed it into locally generated HTML.

## Original asset

[anyx-logo.png](assets/brand/anyx-logo.png) is the user-provided 1024×1024 RGBA image, 1,303,035 bytes. Its SHA-256 is `4b898fa294753d522b6a5c39475f0a430e01b5127cb0bfb39e208d29b80d3f43`.

Preserve the original transparency, glow and yellow-green/cyan/blue appearance. Scale the complete image proportionally with `object-fit: contain`; do not crop, recolor, stretch, recreate or replace the transparent master with a flattened image. PDF and video exports naturally composite it over the artifact background. The portable renderers use a compact 56×56-pixel logo beside “ANYX AGENT KIT”. Adjust placement for the artifact while keeping project content, evidence and coverage readable. These are practical layout choices, not newly specified official brand colors or licensing terms.

## Portable copies and output

The canonical repository asset lives in `assets/brand/`. Each dashboard, presentation and video skill has a byte-identical `assets/brand/anyx-logo.png` copy so an installed skill needs no repository path or network fetch. Its local helper embeds that PNG as a data URI. The HTML deck uses one persistent logo layer across slides and the video composition uses one across scenes. Logo transparency is preserved; the artifact's existing page background remains visible through it.

PNG is packaged as binary without newline normalization. Tests compare decoded output images and extracted ZIP assets against the original SHA-256, rather than merely checking for a logo filename.

## Release boundary

Version `0.1.0-alpha.2` adds branding only. The separately prepared post-review validation and timing fixes are not included. Existing alpha.1 artifacts remain historical unless regenerated and checked. A branded HTML composition is not evidence that a new MP4 was rendered, and neither artifact generation nor logo use authorizes publication or sending.
