#!/usr/bin/env python3
"""Local word-level transcription (faster-whisper on CPU; no API key, nothing leaves the machine).

usage: words.py [--lang pt] [--model small] audio_or_video [...]
Writes <file>.words.json = [{"w": "word", "s": start_s, "e": end_s}, ...] next to each input and prints the text.
The first run downloads the model from huggingface.co (~460 MB for "small"; "medium" is more accurate, ~1.5 GB).
Audio is decoded with ffmpeg (not PyAV), so any format ffmpeg reads works.
"""
import sys, json, argparse, subprocess
import numpy as np
from faster_whisper import WhisperModel

def load(path, sr=16000):
    raw = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', path, '-vn', '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0

def transcribe(files, lang='pt', model='small'):
    m = WhisperModel(model, device='cpu', compute_type='int8')
    out = {}
    for f in files:
        segs, _ = m.transcribe(load(f), language=lang, word_timestamps=True, vad_filter=False, beam_size=5,
                               condition_on_previous_text=False)
        W = [{'w': w.word.strip(), 's': round(w.start, 3), 'e': round(w.end, 3)}
             for s in segs for w in (s.words or []) if w.word.strip()]
        json.dump(W, open(f + '.words.json', 'w'), ensure_ascii=False)
        out[f] = W
    return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='+'); ap.add_argument('--lang', default='pt'); ap.add_argument('--model', default='small')
    a = ap.parse_args()
    for f, W in transcribe(a.files, a.lang, a.model).items():
        print(f'{f}: {len(W)} words\n' + ' '.join(x['w'] for x in W))
