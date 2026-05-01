# Honeymoon Blog

A simple, beautiful honeymoon travel blog. Edit `src/index.html` to add your entries, photos, and story.

## Project Structure

```
honeymoon-blog/
├── src/
│   └── index.html       # Your blog — edit this!
├── tests/
│   └── test_blog.py     # Basic HTML tests
├── Jenkinsfile          # CI/CD pipeline
└── README.md
```

## Customising the Blog

Open `src/index.html` and look for these placeholders:

- **"Your Names"** — replace with your names throughout
- **"Destination"** — replace with where you're going
- **"Year"** — your honeymoon year
- **"Add your travel dates here"** — your actual dates
- **Journal entries** — copy the `<article class="post">` blocks and fill in your own words
- **Photos** — replace `<div class="photo-placeholder">` with `<img>` tags
- **Quote** — add something meaningful to you both

## Jenkins Pipeline

The pipeline has 4 stages:
1. **Checkout** — pulls latest code from GitHub
2. **Test** — runs `tests/test_blog.py` to validate the HTML
3. **Build** — copies `src/` into a `dist/` folder
4. **Deploy** — copies `dist/` to `/var/www/honeymoon-blog`

## Setting Up in Jenkins

1. Create a new **Pipeline** job in Jenkins
2. Under **Pipeline**, set **Definition** to "Pipeline script from SCM"
3. Set SCM to **Git** and add your repo URL
4. Set **Script Path** to `Jenkinsfile`
5. Under **Build Triggers**, enable **Poll SCM** with schedule `H/5 * * * *`

## Serving the Blog

On your Pi, serve the deployed files with Nginx or Python:

```bash
# Quick test with Python
cd /var/www/honeymoon-blog && python3 -m http.server 8081

# Or add an Nginx config pointing to /var/www/honeymoon-blog
```
