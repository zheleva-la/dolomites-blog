#!/usr/bin/env python3
"""Basic tests for the honeymoon blog."""
import sys
import os

def test_file_exists():
    assert os.path.exists("src/index.html"), "index.html not found"
    print("✓ index.html exists")

def test_html_structure():
    with open("src/index.html") as f:
        content = f.read()
    assert "<!DOCTYPE html>" in content, "Missing DOCTYPE"
    assert "<html" in content, "Missing <html>"
    assert "<head>" in content, "Missing <head>"
    assert "<body>" in content, "Missing <body>"
    assert "</html>" in content, "Missing closing </html>"
    print("✓ HTML structure valid")

def test_required_sections():
    with open("src/index.html") as f:
        content = f.read()
    assert 'id="journal"' in content, "Missing journal section"
    assert 'id="photos"' in content, "Missing photos section"
    assert 'id="about"' in content, "Missing about section"
    print("✓ Required sections present")

def test_meta_tags():
    with open("src/index.html") as f:
        content = f.read()
    assert 'charset="UTF-8"' in content, "Missing charset meta"
    assert 'name="viewport"' in content, "Missing viewport meta"
    print("✓ Meta tags present")

if __name__ == "__main__":
    tests = [test_file_exists, test_html_structure, test_required_sections, test_meta_tags]
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
    if failed:
        print(f"\n{failed} test(s) failed.")
        sys.exit(1)
    else:
        print(f"\nAll {len(tests)} tests passed.")
