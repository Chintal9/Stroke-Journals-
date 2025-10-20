# Stroke Landmark Trials RSS

Automatically builds a **PubMed RSS feed** for high-impact, recent stroke trials, guidelines, and major studies. Publishes weekly to GitHub Pages for easy Notion embedding.

## Setup (5 steps)

1. **Upload these files** to your repo:  
   - `main.py`
   - `config.json`
   - `.github/workflows/build.yml`
   - `docs/feed.xml`
   - `README.md`
2. **Enable GitHub Pages**  
   - Settings → Pages → Deploy from branch → select your default branch and `/docs` folder.
3. **Add a repository secret**  
   - Settings → Secrets and variables → Actions → New secret  
   - Name: `GH_TOKEN`  
   - Value: a personal access token with `contents:write` or classic `repo` scope.
4. **Customize the query or title**  
   - Edit `config.json` to change the PubMed query, max results, or feed metadata.
5. **Get your RSS feed URL:**  
   ```
   https://Chintal9.github.io/Stroke-Journals-/feed.xml
   ```

## How it works

- **Python script** queries PubMed for your criteria, builds RSS in `docs/feed.xml` (with TLDR summary).
- **GitHub Action** runs every Monday at midnight UTC, pushes updates.
- **GitHub Pages** serves your RSS feed for Notion or any RSS reader.

## Custom Formatting

- Each item shows:  
  - Journal name  
  - Authors  
  - TLDR summary (first 40 words of abstract)  
  - Full abstract  
  - Link to PubMed

## Notion Embedding

- In Notion, type `/embed` and paste your feed URL.

## Advanced

- To use AI summaries for TLDR, update `main.py` to call your summarization API.

---

Questions? Open an issue or ask!