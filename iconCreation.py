from PIL import Image, ImageEnhance


def generate_padded_cube(texture_path, output_path):
    scale_ratio = 1.1
    # 1. Load and Scale Up Texture (Crucial for crisp edges)
    # We upscale the input texture to ensure the math has enough pixels to work with
    img = Image.open(texture_path).convert("RGBA")
    s = img.width * 4
    img = img.resize((s, s), Image.NEAREST)

    # 2. Define Canvas Size (Fixed at 100% scale)
    # A standard isometric cube fits in a width of 2*s and height of ~3*s
    # We lock the canvas to this size so the image doesn't shrink.
    canvas_w = s * 2
    canvas_h = s * 3
    
    # Center point of the canvas
    cx, cy = canvas_w // 2, canvas_h // 2

    # 3. Define Cube Geometry (Scaled by scale_ratio)
    # We shrink the drawing logic, not the canvas
    w = int(s * scale_ratio)       # Scaled Width
    h = int((s // 2) * scale_ratio) # Scaled Height Step
    v = int(s * scale_ratio)       # Scaled Vertical Drop

    # 4. Prepare Textures (Same as before)
    top_tex = img
    right_tex = ImageEnhance.Brightness(img).enhance(0.7)
    left_tex = ImageEnhance.Brightness(img).enhance(0.5)

    # 5. Affine Transform Helper
    def apply_transform(tex, p_out):
        (x0, y0), (x1, y1), (x2, y2) = p_out
        c, f = x0, y0
        
        # We use 's' (original texture size) here because the source texture is still full size
        a = (x1 - c) / s
        d = (y1 - f) / s
        b = (x2 - c) / s
        e = (y2 - f) / s
        
        det = a*e - b*d
        if det == 0: return tex 

        ia, ib, ic = e/det, -b/det, (b*f - c*e)/det
        id, ie, if_ = -d/det, a/det, (c*d - a*f)/det
        
        # Transform into the full canvas size
        return tex.transform((canvas_w, canvas_h), Image.AFFINE, 
                           (ia, ib, ic, id, ie, if_), 
                           resample=Image.NEAREST)

    # 6. Calculate Points (Centered)
    # Top Face
    top_pts = [(cx, cy - 2*h), (cx + w, cy - h), (cx - w, cy - h)]
    
    # Right Face
    right_pts = [(cx, cy), (cx + w, cy - h), (cx, cy + v)]
    
    # Left Face
    left_pts = [(cx - w, cy - h), (cx, cy), (cx - w, cy - h + v)]

    # 7. Render
    top_face = apply_transform(top_tex, top_pts)
    right_face = apply_transform(right_tex, right_pts)
    left_face = apply_transform(left_tex, left_pts)

    final = Image.new("RGBA", (canvas_w, canvas_h))
    final.paste(top_face, (0, 0), top_face)
    final.paste(right_face, (0, 0), right_face)
    final.paste(left_face, (0, 0), left_face)

    # 8. Final Crop (Optional: Remove ONLY the excess space beyond the 100% canvas logic)
    # Since we want to keep the "100% size" frame, we don't use .getbbox() here.
    # However, if you want to trim the pure empty top/bottom from the 3*s calculation:
    # We can crop to the 'theoretical' max size:
    max_h = int(s * 2.5) # Approximate height of a full cube
    max_w = int(s * 2.5)   # Width remains the same
    final = final.crop(((canvas_w - max_w)//2, (canvas_h - max_h)//2,  (canvas_w + max_w)//2, (canvas_h + max_h)//2))

    # Resize back down to original texture scale if desired (e.g., if you started with 16x16)
    final = final.resize((img.width // 4 * 4, int(img.width // 4 * 4)), Image.LANCZOS)
    
    final.save(output_path)
