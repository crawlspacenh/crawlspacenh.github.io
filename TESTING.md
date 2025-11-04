# Testing Guide

This repository includes automated tests that run on every pull request to ensure the site builds correctly and doesn't have common issues.

## GitHub Actions (Automatic)

Tests run automatically on every pull request via GitHub Actions. The workflow checks:

1. **Front Matter Validation** - Ensures TOML syntax is correct in all content files
2. **Build Validation** - Verifies Hugo can build the site without errors
3. **Build Output Verification** - Confirms expected files are generated
4. **Internal Link Checking** - Detects broken internal links using htmltest
5. **HTML Structure Validation** - Checks for proper HTML structure

You can view test results in the "Actions" tab of the GitHub repository or on the pull request page.

## Running Tests Locally

Before pushing changes, you can run the same tests locally to catch issues early.

### Prerequisites

**Required:**
- [Hugo](https://gohugo.io/installation/) (Extended version 0.151.2 or compatible)

**Optional (but recommended):**
- [htmltest](https://github.com/wjdp/htmltest) - For checking broken links

#### Installing htmltest

**macOS:**
```bash
brew install htmltest
```

**Linux:**
```bash
wget https://github.com/wjdp/htmltest/releases/download/v0.17.0/htmltest_0.17.0_linux_amd64.tar.gz
tar -xzf htmltest_0.17.0_linux_amd64.tar.gz
sudo mv htmltest /usr/local/bin/
```

**Windows:**
Download from [releases page](https://github.com/wjdp/htmltest/releases) and add to PATH.

### Running the Test Suite

From the repository root, run:

```bash
./scripts/test.sh
```

The script will:
- Check Hugo is installed
- Validate front matter in content files
- Build the site with production settings
- Verify build output
- Check CNAME configuration
- Run htmltest (if installed) to detect broken links
- Validate HTML structure

### Understanding Test Output

The test script provides colored output:
- ✓ Green - Tests passed
- ✗ Red - Tests failed (must fix)
- ⚠ Yellow - Warnings (should review)
- ℹ Blue - Informational messages

### Test Exit Codes

- `0` - All tests passed
- `1` - One or more tests failed

### Quick Pre-Push Check

Add this to your workflow before pushing:

```bash
# Build and test locally
./scripts/test.sh

# If tests pass, commit and push
git add .
git commit -m "Your commit message"
git push origin your-branch
```

### Common Issues

**Hugo not found:**
- Install Hugo from https://gohugo.io/installation/
- Ensure you have the Extended version

**Front matter errors:**
- Check TOML syntax in content/*.md files
- Ensure dates are properly formatted
- Verify all quotes are matched

**Build failures:**
- Check for missing images referenced in content
- Verify theme files are present (submodules)
- Review Hugo error messages for specific issues

**Broken links:**
- Update internal links to point to existing pages
- Check that file names match link references
- Remember Hugo uses .html extensions in production build

## Continuous Integration

The test workflow (`.github/workflows/pr-tests.yml`) uses the exact same Hugo version and build settings as the deployment workflow to ensure consistency between testing and production.

### Workflow Files

- `.github/workflows/hugo.yaml` - Deploys to GitHub Pages on push to main
- `.github/workflows/pr-tests.yml` - Runs tests on pull requests

## Adding New Tests

To add new tests:

1. Update `.github/workflows/pr-tests.yml` to add the test step
2. Update `scripts/test.sh` to include the same test for local execution
3. Document the new test in this file

Keep tests fast and focused on catching real issues that would break the site or degrade user experience.
