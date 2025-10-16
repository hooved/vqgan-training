import io, os
from PIL import Image
from tqdm import tqdm
import webdataset as wds
from pathlib import Path

DIR_IN = Path("/raid/datasets/imagenet")
DIR_OUT = Path("/raid/datasets/imagenet_wds")
SYNSET    = "n03733281"
CLASS_ID  = 646
LABEL     = "maze"

SRC_DIR   = f"/raid/datasets/imagenet/train/{SYNSET}"
OUT_TAR   = f"/raid/datasets/imagenet_wds/train/{SYNSET}.tar"  # single shard output

def img_paths(root, exts=(".JPEG",)):
  for f in sorted(os.listdir(root)):
    if f.endswith(exts): yield os.path.join(root, f)

def main():
  os.makedirs(DIR_OUT, exist_ok=True)
  for phase in ("train", "val"):
    if phase == "train": continue
    sink = wds.TarWriter(str(DIR_OUT / f"{SYNSET}_{phase}.tar"))
    for p in tqdm(list(img_paths(str(DIR_IN / phase / SYNSET))), desc="writing shard"):
        buf = io.BytesIO()
        Image.open(p).convert("RGB").save(buf, "PNG")
        key = Path(p).stem
        assert p.endswith(".JPEG") and p.count(".JPEG") == 1
        sample = {
        "__key__": key,
        "png": buf.getvalue(),
        "id": f"{CLASS_ID}\n".encode(),
        "label": LABEL.encode(),
        "synset": SYNSET.encode(),
        }
        sink.write(sample)
    sink.close()

if __name__ == "__main__":
  main()