#!/usr/bin/env python3
import os
import sys
import zipfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.zip_export import zip_files, zip_epub_batch


def test_zip_files_creates_archive(tmp_path):
    f1 = tmp_path / "book1.epub"
    f2 = tmp_path / "book2.epub"
    f1.write_bytes(b"epub1")
    f2.write_bytes(b"epub2")
    out = str(tmp_path / "output.zip")
    result = zip_files([str(f1), str(f2)], out)
    assert result is not None
    assert os.path.exists(result)
    with zipfile.ZipFile(result) as z:
        assert "book1.epub" in z.namelist()
        assert "book2.epub" in z.namelist()


def test_zip_files_returns_none_when_no_valid_files(tmp_path):
    out = str(tmp_path / "empty.zip")
    result = zip_files(["/nonexistent/file.epub"], out)
    assert result is None
    assert not os.path.exists(out)  # empty archive deleted


def test_zip_files_count_matches(tmp_path):
    files = []
    for i in range(5):
        f = tmp_path / f"book{i}.epub"
        f.write_bytes(b"x")
        files.append(str(f))
    out = str(tmp_path / "batch.zip")
    zip_files(files, out)
    with zipfile.ZipFile(out) as z:
        assert len(z.namelist()) == 5


def test_zip_epub_batch_from_job_store(tmp_path):
    f1 = tmp_path / "a.epub"
    f2 = tmp_path / "b.epub"
    f1.write_bytes(b"a")
    f2.write_bytes(b"b")
    store = {"batch_abc": {"epub_files": [str(f1), str(f2)]}}
    result = zip_epub_batch("batch_abc", store, output_dir=tmp_path)
    assert result is not None
    assert result.endswith(".zip")
    with zipfile.ZipFile(result) as z:
        assert len(z.namelist()) == 2


def test_zip_epub_batch_missing_job_returns_none():
    assert zip_epub_batch("nonexistent", {}) is None


def test_zip_epub_batch_empty_epub_list_returns_none(tmp_path):
    store = {"batch_xyz": {"epub_files": []}}
    assert zip_epub_batch("batch_xyz", store, output_dir=tmp_path) is None
