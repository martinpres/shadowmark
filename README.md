# Shadowmark

A tool for blind image watermarking based on differential embedding in DWT and DCT domains[[1]](#1). This tool supports
embedding an RGB watermark into a target image and extracting it back without needing the original image.

## Installation

Clone this repository and install the package with pip. Use of virtual environment is recommended.

```bash
git clone git@github.com:martinpres/shadowmark.git shadowmark
cd shadowmark
pip install .
```

## Usage

Let's use an input image and a watermark:

| Original image<br/>(800x603)                                    | Watermark<br/>(32x32)                       |
|-----------------------------------------------------------------|---------------------------------------------|
| <img src="blob/media/image.png" alt="Original image" width=256> | ![Watermark](blob/media/watermark32x32.png) |

To embed the watermark to the input image:

```bash
shadowmark --image image.png --embed watermark32x32.png --output embedded.png
```

To extract the watermark from the image:

```bash
shadowmark --image embedded.png --output extracted.png
```

| Watermarked image<br/>(800x603)                                       | Extracted watermark<br/>(32x32)        |
|-----------------------------------------------------------------------|----------------------------------------|
| <img src="blob/media/embedded.png" alt="Watermarked image" width=256> | ![Watermark](blob/media/extracted.png) |

### RGB channels

You can choose specific RGB channel that will be used for embedding by using the `--channels` parameter. This may be
used for both embedding and extraction or just for the extraction. Extraction of different channels than were embedded
yields just noise. Supported channels are red ('r'), green ('g') and blue ('b').

```bash
shadowmark --image image.png --embed watermark32x32.png --output embedded.png --channels g 
shadowmark --image embedded.png --output extracted.png --channels g
```

| Watermarked image<br/>channel = g<br/>(800x603)                                                                  | Extracted watermark<br/>channel = g<br/>(32x32)  |
|------------------------------------------------------------------------------------------------------------------|--------------------------------------------------|
| <img src="blob/media/embedded-channel_g.png" alt="Image with watermark embedded in the green channel" width=256> | ![Watermark](blob/media/extracted-channel_g.png) |

You may also specify combination of channels:

```bash
shadowmark --image image.png --embed watermark32x32.png --output embedded.png --channels rg
shadowmark --image embedded.png --output extracted.png --channels rg
```

| Watermarked image<br/>channel = rg<br/>(800x603)                                                                           | Extracted watermark<br/>channel = rg<br/>(32x32)  |
|----------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------|
| <img src="blob/media/embedded-channel_rg.png" alt="Image with watermark embedded in the red and green channels" width=256> | ![Watermark](blob/media/extracted-channel_rg.png) |

### Robustness

By default, the extracted watermark may not always perfectly match the embedded one, but you may use the `--gain`
parameter to increase robustness of the embedding:

```bash
shadowmark --image image.png --embed watermark32x32.png --output embedded.png --gain 3
shadowmark --image embedded.png --output extracted.png
```

| Watermarked image<br/>gain = 3<br/>(800x603)                                                  | Extracted watermark<br/>gain = 3<br/>(32x32)  |
|-----------------------------------------------------------------------------------------------|-----------------------------------------------|
| <img src="blob/media/embedded-gain_3.png" alt="Watermarked image with higher gain" width=256> | ![Watermark](blob/media/extracted-gain_3.png) |

Note that higher gain values introduce more noise into the watermarked image, which can reduce its visual quality.

### Different watermark sizes

The watermark image is by default 32x32 pixels. You may use different sizes, but larger watermarks make the watermarked
image even noisier. The watermark size is not automatically encoded in the watermarked image, and you must specify it by
the `--extract WxH` parameter:

```bash
shadowmark --image image.png --embed watermark64x64.png --output embedded.png
shadowmark --image embedded.png --extract 64x64 --output extracted.png
```

| Watermarked image<br/>(800x603)                                                                   | Extracted watermark<br/>(64x64)              |
|---------------------------------------------------------------------------------------------------|----------------------------------------------|
| <img src="blob/media/embedded-64x64.png" alt="Image watermarked with larger watermark" width=256> | ![Watermark](blob/media/extracted-64x64.png) |

### Seed for protection

The watermark is embedded the same way every time by default and an attacker that knows the implementation, size, gain
and channels may tamper with the watermark and damage it. To minimize the risk, you may use the `--seed` parameter to
specify a seed for the internal RNG:

```bash
shadowmark --image image.png --embed watermark32x32.png --output embedded.png --seed 20241224122442
shadowmark --image embedded.png --output extracted.png --seed 20241224122442
```

| Watermarked image<br/>seed = 20241224122442<br/>(800x603)                            | Extracted watermark<br/>correct seed<br/>(32x32)    | Extracted watermark<br/>incorrect seed<br/>(32x32)    |
|--------------------------------------------------------------------------------------|-----------------------------------------------------|-------------------------------------------------------|
| <img src="blob/media/embedded-seed.png" alt="Watermarked image with seed" width=256> | ![Watermark](blob/media/extracted-correct_seed.png) | ![Watermark](blob/media/extracted-incorrect_seed.png) |

> **Warning:**
> The seed parameter does not provide strong cryptographic protection.

## Resistance to attacks

| Attack                     | Example   <br/>gain = 1                                                                  | Extracted watermark<br/>gain = 1<br/>(32x32 )                    | Example   <br/>gain = 5                                                                  | Extracted watermark<br/>gain = 5<br/>(32x32 )                    |
|----------------------------|------------------------------------------------------------------------------------------|------------------------------------------------------------------|------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| Grayscale                  | <img src="blob/media/gain_1-attack-grayscale.png" alt="Grayscale attack" width=256>      | ![Watermark](blob/media/gain_1-extracted-attack-grayscale.png)   | <img src="blob/media/gain_5-attack-grayscale.png" alt="Grayscale attack" width=256>      | ![Watermark](blob/media/gain_5-extracted-attack-grayscale.png)   |
| JPEG quality 60%           | <img src="blob/media/gain_1-attack-jpeg_60.jpg" alt="JPEG compression attack" width=256> | ![Watermark](blob/media/gain_1-extracted-attack-jpeg_60.jpg)     | <img src="blob/media/gain_5-attack-jpeg_60.jpg" alt="JPEG compression attack" width=256> | ![Watermark](blob/media/gain_5-extracted-attack-jpeg_60.jpg)     |
| Obstructing parts of image | <img src="blob/media/gain_1-attack-obstruction.png" alt="Obstruction attack" width=256>  | ![Watermark](blob/media/gain_1-extracted-attack-obstruction.png) | <img src="blob/media/gain_5-attack-obstruction.png" alt="Obstruction attack" width=256>  | ![Watermark](blob/media/gain_5-extracted-attack-obstruction.png) |
| Cropping                   | <img src="blob/media/gain_1-attack-crop.png" alt="Crop attack" width=256>                | ![Watermark](blob/media/gain_1-extracted-attack-crop.png)        | <img src="blob/media/gain_5-attack-crop.png" alt="Crop attack" width=256>                | ![Watermark](blob/media/gain_5-extracted-attack-crop.png)        |
| Flipping horizontally      | <img src="blob/media/gain_1-attack-flip.png" alt="Flip attack" width=256>                | ![Watermark](blob/media/gain_1-extracted-attack-flip.png)        | <img src="blob/media/gain_5-attack-flip.png" alt="Flip attack" width=256>                | ![Watermark](blob/media/gain_5-extracted-attack-flip.png)        |
| Rotation                   | <img src="blob/media/gain_1-attack-rotation.png" alt="Rotation attack" width=256>        | ![Watermark](blob/media/gain_1-extracted-attack-rotation.png)    | <img src="blob/media/gain_5-attack-rotation.png" alt="Rotation attack" width=256>        | ![Watermark](blob/media/gain_5-extracted-attack-rotation.png)    |
| Resize to half             | <img src="blob/media/gain_1-attack-resize.png" alt="Resize attack" width=256>            | ![Watermark](blob/media/gain_1-extracted-attack-resize.png)      | <img src="blob/media/gain_5-attack-resize.png" alt="Resize attack" width=256>            | ![Watermark](blob/media/gain_5-extracted-attack-resize.png)      |

## References

<a id="1">[1]</a>: Benoraira, A., Benmahammed, K. & Boucenna, N. Blind image watermarking technique based on
differential embedding in DWT and DCT domains. EURASIP J. Adv. Signal Process. 2015, 55 (
2015). https://doi.org/10.1186/s13634-015-0239-5
