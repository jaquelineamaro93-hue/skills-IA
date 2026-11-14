"""Gera output/*.srt a partir de src/timeline.json (mesma lógica de src/components/Subtitles.tsx)."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
tl = json.loads((root / "src/timeline.json").read_text())
ev = {e["id"]: e["at"] for e in tl["voiceEvents"]}
cues = []
for s in tl["subtitles"]:
    c = tl["voiceClips"][s["voice"]]; at = ev[s["voice"]]
    a, b = at + 0.02, at + (c["out"] - c["in"]) + 0.12
    if "parts" in s:
        cues += [(a, at + s["split"], s["parts"][0]["lines"]), (at + s["split"], b, s["parts"][1]["lines"])]
    else:
        cues.append((a, b, s["lines"]))
def ts(x):
    ms = int(round(x * 1000)); return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"
out = "\n".join(f"{i}\n{ts(a)} --> {ts(b)}\n" + "\n".join(l.replace("*", "") for l in L) + "\n" for i, (a, b, L) in enumerate(cues, 1))
(root / "output/camilo-ep01-legendas-pt-BR.srt").write_text(out, encoding="utf-8")
# versão com as falas originais em espanhol (transcrição), útil para a edição
orig = "\n".join(f"{i}\n{ts(ev[k])} --> {ts(ev[k] + c['out'] - c['in'])}\n[{'NARRADOR' if c['speaker']=='narrador' else 'CAMILO'}] {c['text']}\n"
                 for i, (k, c) in enumerate(sorted(tl["voiceClips"].items(), key=lambda kv: ev[kv[0]]), 1))
(root / "output/camilo-ep01-falas-originais.srt").write_text(orig, encoding="utf-8")
print(len(cues), "legendas")
