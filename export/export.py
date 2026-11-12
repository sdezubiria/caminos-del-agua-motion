"""Exports the logo and card animations as videos (on their coloured backgrounds) and transparent PNG sequences.

    python3 export.py OUT_DIR [WORK_DIR]

OUT_DIR gets the deliverables; WORK_DIR (default: a temp folder) holds the full-page frames used only for its video.
"""
import json, pathlib, re, subprocess, sys, tempfile, unicodedata

HERE = pathlib.Path(__file__).resolve().parent
FPS = 30
CIELO, LOGO_BG = '9ECFEB', 'F9F9F2'   # logo video on the site's crema
FFMPEG_MP4 = ['-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart']


def render(out, scene, w, h, frames, query=''):
    subprocess.run([sys.executable, str(HERE / 'render.py'), str(out), scene, str(w), str(h), str(frames), str(FPS)] + ([query] if query else []), check=True)


def ffmpeg(*args):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *args], check=True)


def slug(s):
    s = unicodedata.normalize('NFKD', s.replace('<br>', ' ')).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def card_titles():
    src = (HERE.parent / 'assets/cards-data.js').read_text()
    return [(int(n), t) for n, t in re.findall(r"n: (\d), title: '([^']*)'", src)]


def main():
    out = pathlib.Path(sys.argv[1])
    work = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else pathlib.Path(tempfile.mkdtemp(prefix='cda-export-'))

    # Logo: one cycle is 22/9 s, so 3 cycles = 220 frames at 30 fps loop seamlessly
    d = out / '01_logo-corriente'
    seq = d / 'logo-corriente_png'
    render(seq, 'logo', 1964, 1704, 220)
    ffmpeg('-f', 'lavfi', '-i', f'color=c=0x{LOGO_BG}:s=1920x1080:r={FPS}', '-framerate', str(FPS), '-i', str(seq / 'logo-corriente_%04d.png'),
           '-filter_complex', '[1]scale=-1:822:flags=lanczos[l];[0][l]overlay=(W-w)/2:(H-h)/2:shortest=1', *FFMPEG_MP4, str(d / 'logo-corriente_1920x1080.mp4'))

    # Cards: 5 s loop each (front, flip, photo side, flip back), 1080 × 1920
    for n, title in card_titles():
        name = f'raiz-{n}_{slug(title)}'
        d = out / '02_tarjetas' / name
        seq = d / f'{name}_png'
        render(seq, 'card', 1080, 1920, 5 * FPS, f'n={n}')
        ffmpeg('-f', 'lavfi', '-i', f'color=c=0x{CIELO}:s=1080x1920:r={FPS}', '-framerate', str(FPS), '-i', str(seq / f'{name}_%04d.png'),
               '-filter_complex', '[0][1]overlay=0:0:shortest=1', *FFMPEG_MP4, str(d / f'{name}_1080x1920.mp4'))

    # Whole "Nuestra Visión: Siete Raíces" page, same 17 s loop as the site
    seq = work / 'siete-raices'
    render(seq, 'page', 1920, 2378, 17 * FPS)
    d = out / '03_siete-raices-completo'
    d.mkdir(parents=True, exist_ok=True)
    ffmpeg('-framerate', str(FPS), '-i', str(seq / 'siete-raices_%04d.png'), *FFMPEG_MP4, str(d / 'siete-raices_1920x2378.mp4'))
    print('done:', out)


if __name__ == '__main__':
    main()
