# Copy of PLAN.md section 14. Lives in the root of the ielts-content repository.
import hashlib, json, pathlib

root = pathlib.Path(__file__).parent
tests = []
for d in sorted((root / "tests").glob("test-*")):
    meta = json.loads((d / "meta.json").read_text())
    files = []
    for p in sorted(d.rglob("*")):
        if p.is_file() and p.name != "meta.json" and p.suffix in {".json", ".mp3", ".png"}:
            files.append({
                "path": p.relative_to(root).as_posix(),
                "bytes": p.stat().st_size,
                "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            })
    tests.append({"id": d.name, "number": meta["number"], "title": meta["title"],
                  "releaseDate": meta["releaseDate"], "files": files})
(root / "index.json").write_text(json.dumps({"schemaVersion": 1, "tests": tests}, indent=1))
print(len(tests), "tests indexed")
