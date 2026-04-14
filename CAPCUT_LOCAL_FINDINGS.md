# CapCut Local Data Scan - Comprehensive Findings

> Scanned: `C:\Users\DELL\AppData\Local\CapCut` (App v8.4.0.3562)

---

## 1. Data Source Map

| Location | Type | Count | Usability |
|----------|------|-------|-----------|
| `User Data/Cache/effect/{id}/{md5}/config.json` | Effect configs | 380+ | ✅ JSON readable |
| `User Data/Projects/com.lveditor.draft/*/draft_content.json` | Draft JSONs | 16 drafts | ✅ JSON readable |
| `User Data/Resources/MixMode/MixMode.json` | Blend modes | 10 | ✅ JSON readable |
| `User Data/Config/Modules/beauty_panels_en.ini` | Beauty/Face effects | 96 face keys, 5 body keys | ⚠️ Qt @Variant (parseable) |
| `Apps/8.4.0.3562/Resources/lut/config.json` | LUT/Filters | ~20+ | ✅ JSON readable |
| `User Data/Resources/Font/SystemFont/` | Built-in fonts | 17 | ✅ Font files |
| `User Data/Cache/effect/model/` | AI models | 55+ | ❌ Binary models |
| `User Data/Cache/agencycache/` | Video templates | 12 pairs | ⚠️ .agency + .mp4 |
| `User Data/Cache/AigcMaterailCache/` | AIGC materials | 13 | ❌ Unknown format |
| `User Data/Config/Modules/*.ini` | Config panels | 15 files | ⚠️ Qt @Variant |
| `User Data/Cache/resourcePanel/` | Resource catalog | many | ❌ Binary protobuf |

---

## 2. Effect Cache (HIGHEST VALUE)

**Path**: `Cache/effect/{resource_id}/{md5}/config.json`

380+ cached effects. Each `config.json` contains:
```json
{
  "effect": {
    "Link": [{
      "type": "AmazingFeature|InfoSticker|GeneralEffect|matting",
      "path": "local_path",
      "zorder": 0,
      "extra": {
        "composer_param": [{
          "name": "param_display_name",
          "key": "param_key",
          "default_value": 0.5,
          "min_value": 0.0,
          "max_value": 1.0
        }]
      }
    }]
  },
  "name": "Effect Name",
  "version": "1.0"
}
```

**Types discovered:**
- **157 AmazingFeature** (AR/face effects with shader parameters)
- **37 InfoSticker** (animated sticker overlays)
- **1 GeneralEffect** (basic scene effects)
- **1 Matting** (background removal)

**→ ACTION**: Write scanner to batch-read all `config.json` and output metadata for `capcut_effect_meta.py`.

---

## 3. Draft Extraction Results

From 16 local drafts:

| Type | Found | Details |
|------|-------|---------|
| Transitions | 4 | `Dissolve` (resource_id=6724846004274729480) |
| Effects | 27 | All `text_effect` type |
| Animations | 9 | Flash In / Flash Out / various |
| Audio Effects | 0 | — |
| Video Effects | 0 | — |
| Stickers | 0 | — |
| Filters | 0 | — |

**→ ACTION**: Use `reverse_engineer.py` on more drafts that contain varied effects.

---

## 4. Beauty/Face Panel (96 Effect Keys)

Extracted from `beauty_panels_en.ini` (Qt @Variant format).

### INI Sections:
- `[auto-beauty]`, `[auto-beauty2]`, `[auto-beauty3]` — Auto beauty presets
- `[face_shape]` — Face reshaping
- `[facial_features]` — Facial feature adjustments
- `[makeup]` — Full makeup panel
- `[makeup_root]` — Makeup root config (Lipstick)
- `[manual-figure]` — Body reshaping (Stretch, Slim, Enhance)
- `[manual_beauty]` — Manual beauty controls
- `[skinColor]`, `[skinColorNew]` — Skin color adjustment
- `[skin_management]` — Skin management
- `[face_box]` — Face detection box

### All 96 Face Adjust Keys:
```
CATEGORY: Blusher (Blush)
  face_adjust_blusher (root)
  face_adjust_blusher_chumeisaihong
  face_adjust_blusher_chunrijusaihong
  face_adjust_blusher_fentao
  face_adjust_blusher_liangju
  face_adjust_blusher_sizi
  face_adjust_blusher_yemeifensaihong
  face_adjust_blusher_yingerfen
  face_adjust_blusher_yingguangfen

CATEGORY: Eyebrow
  face_adjust_brow (root)
  face_adjust_brow_distance
  face_adjust_brow_gaotiaomei
  face_adjust_brow_guyunmeifree
  face_adjust_brow_position
  face_adjust_brow_ridge
  face_adjust_brow_rongrongmei
  face_adjust_brow_tilt
  face_adjust_brow_xitiaomei
  face_adjust_brow_yeshengmei
  face_adjust_brow_yeshengmeiii

CATEGORY: Eyelash
  face_adjust_eyelash (root)
  face_adjust_eyelash_cateye
  face_adjust_eyelash_kpop
  face_adjust_eyelash_latina
  face_adjust_eyelash_lingdong
  face_adjust_eyelash_wanggan
  face_adjust_eyelash_xianzimao
  face_adjust_eyelash_xiaoemo
  face_adjust_eyelash_yanxi
  face_adjust_eyelash_ziran

CATEGORY: Eye Effects
  face_adjust_eyelight
  face_adjust_inner_corner

CATEGORY: Eyeliner
  face_adjust_eyeline (root)
  face_adjust_eyeline_doubleoumei
  face_adjust_eyeline_oumeixiake
  face_adjust_eyeline_oumeiyanshi
  face_adjust_eyeline_qizhi
  face_adjust_eyeline_wumeioumei
  face_adjust_eyeline_xiaoyemaooumei

CATEGORY: Eyeshadow
  face_adjust_eyeshadow (root)
  face_adjust_eyeshadow_jiazhouriluo
  face_adjust_eyeshadow_jipusai
  face_adjust_eyeshadow_luozhuang
  face_adjust_eyeshadow_naiyoufenzhong
  face_adjust_eyeshadow_richangju
  face_adjust_eyeshadow_shashouyanxun
  face_adjust_eyeshadow_wugu

CATEGORY: Lips
  face_adjust_fengchun
  face_adjust_lip (root)
  face_adjust_lip_dianguanglan
  face_adjust_lip_feiluomeng
  face_adjust_lip_houchun
  face_adjust_lip_meidusha
  face_adjust_lip_monvzi
  face_adjust_lip_nanguatang
  face_adjust_lip_wumian
  face_adjust_lip_yuanqitianyou
  face_adjust_lip_yunran

CATEGORY: Highlights (Contour/Glow)
  face_adjust_highlight (root)
  face_adjust_highlight_fengyinggaoguang
  face_adjust_highlight_gaobilianggaoguang
  face_adjust_highlight_litigaoguang
  face_adjust_highlight_meishigaoguang
  face_adjust_highlight_shuirungaoguang
  face_adjust_highlight_wanggangaoguang

CATEGORY: Freckles/Mask
  face_adjust_mask (root)
  face_adjust_mask_anglequeban
  face_adjust_mask_chaoziranqueban
  face_adjust_mask_jiariqueban
  face_adjust_mask_jipusaiqueban
  face_adjust_mask_meishiqueban
  face_adjust_mask_shaishangqueban

CATEGORY: Pupil/Eye Color
  face_adjust_pupil (root)
  face_adjust_pupil_mihoutaomt
  face_adjust_pupil_shemeitong
  face_adjust_pupil_shuiguanghei
  face_adjust_pupil_tianshengqiantong
  face_adjust_pupil_tianshimeit
  face_adjust_pupil_touguangguang

CATEGORY: Stereo/Contour
  face_adjust_stereo (root)
  face_adjust_stereo_baoman
  face_adjust_stereo_jingzhi
  face_adjust_stereo_litibi
  face_adjust_stereo_pingguoji
  face_adjust_stereo_shensui
  face_adjust_stereo_ziran

CATEGORY: Face Structure
  face_adjust_fuling (face width)
  face_adjust_lower_atrium
  face_adjust_mid_atrium
  face_adjust_upper_atrium
  face_adjust_mouse_corner
  face_adjust_nose_bridge
  face_adjust_nose_position
  face_adjust_nose_root
  face_adjust_skin
  face_adjust_whole
```

### Body Reshaping Keys:
```
  manual_beauty     — Manual beauty root
  manual_deformation — Body deformation
  manual_slim       — Body slimming
  manual_stretch    — Body stretching
  manual_zoom       — Body zoom/enhance
```

### Subcategories Found:
Blush, Eye Color, Eyebrow, Eyelash, Eyeliner, Eyeshadow, Freckles, Highlights, Lipstick, Reshape, etc.

**→ ACTION**: Each key has `effect_id`, `resource_id`, `md5`, `defaultValue`, `minValue=0`, `maxValue=100`, `composer_name=intensity`, path to cache. This is enough to build a `capcut_beauty_meta.py`.

---

## 5. Blend Modes (MixMode)

**Path**: `Resources/MixMode/MixMode.json`

| Name | Resource ID | Effect ID |
|------|-------------|-----------|
| color_filter | 871339 | — |
| dark_en | 871342 | — |
| bright_en | 871341 | — |
| over_lay | 871340 | — |
| glare_pc | 871338 | — |
| soft_light | 871337 | — |
| linear_deepening | 871336 | — |
| darken_color | 871335 | — |
| + 2 more | — | — |

**→ ACTION**: Add `set_blend_mode()` API endpoint. Data is already extracted.

---

## 6. Effect Param Names

**Path**: `effectParamNames.json` in each effect cache

21 standard parameter mappings:
- `effects_adjust_blur` → "Blur"
- `effects_adjust_speed` → "Speed"
- `effects_adjust_color` → "Color"
- `effects_adjust_distortion` → "Distortion"
- `effects_adjust_filter` → "Filter"
- `effects_adjust_intensity` → "Intensity"
- `effects_adjust_luminance` → "Luminance"
- `effects_adjust_noise` → "Noise"
- `effects_adjust_range` → "Range"
- `effects_adjust_rotate` → "Rotate"
- `effects_adjust_sharpen` → "Sharpen"
- `effects_adjust_size` → "Size"
- `effects_adjust_soft` → "Soft"
- `effects_adjust_texture` → "Texture"
- + 7 more

---

## 7. Config Modules (15 .ini files)

| File | Purpose |
|------|---------|
| `adjust_collection.ini` | Color adjustment presets |
| `beauty_panels_en.ini` | **Beauty/face panel (71KB, decoded above)** |
| `camera-movement.ini` | Camera movement presets |
| `camera_tracking.ini` | Camera tracking settings |
| `complex_video_mask.ini` | Advanced video masks |
| `draft_tracking.ini` | Draft tracking config |
| `export_service.ini` | Export/render settings |
| `eye_contact.ini` | Eye contact AI feature |
| `home_page_ratio_select.ini` | Aspect ratio presets |
| `matting.ini` | Background removal settings |
| `matting_config.ini` | Matting model config |
| `player_ruler.ini` | Timeline ruler settings |
| `segment_js_config.ini` | Segment JS config |
| `timeline_settings.ini` | Timeline settings |

**High-value files**: `camera-movement.ini`, `complex_video_mask.ini`, `matting_config.ini`

---

## 8. Fonts

**Path**: `User Data/Resources/Font/SystemFont/`

17 built-in system fonts available for text effects.

---

## 9. AI Models (Info Only)

**Path**: `User Data/Cache/effect/model/`

55+ ML models including:
- Face detection / landmarks
- Background matting / segmentation
- Object tracking
- Face aging / beauty scoring
- Style transfer

These are binary `.model` files — not directly usable by the API but indicate CapCut's AI capabilities.

---

## Priority Recommendations for API Expansion

### P0 - Quick Wins (data already extracted)
1. **Blend Modes** → Add `set_blend_mode()` with 10 modes from MixMode.json
2. **Effect Cache Scanner** → Batch-read 380 `config.json` files to expand `capcut_effect_meta.py`

### P1 - Medium Effort
3. **Beauty/Face effects** → Build `capcut_beauty_meta.py` from the 96 face adjust keys + 5 body keys
4. **More drafts** → Use `reverse_engineer.py` to extract transitions/effects from drafts that use them
5. **Filter/LUT support** → Read `lut/config.json` to add filter presets

### P2 - Advanced
6. **Camera Movement** → Parse `camera-movement.ini` for keyframe animation presets
7. **Complex Masks** → Parse `complex_video_mask.ini` for advanced masking
8. **Font System** → Expose 17 system fonts + custom font loading

### P3 - Research Required
9. **Cross Open transition** → Must be captured via draft (apply in CapCut → read draft JSON)
10. **Network interception** → Capture API calls when CapCut downloads new effects
