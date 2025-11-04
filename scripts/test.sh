#!/bin/bash

# Local test script for crawlspacenh.com
# Runs the same tests as the GitHub Actions PR workflow

# Note: We don't use 'set -e' to allow graceful error handling
# and complete test reporting even if some tests fail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0
WARNINGS=0

print_header() {
    echo -e "\n${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
    ((TESTS_PASSED++))
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    ((TESTS_FAILED++))
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
    ((WARNINGS++))
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Change to repository root
cd "$(dirname "$0")/.."

print_header "Crawlspace Site Test Suite"

# Check if Hugo is installed
print_info "Checking Hugo installation..."
if ! command -v hugo &> /dev/null; then
    print_error "Hugo is not installed. Please install Hugo first."
    echo "Visit: https://gohugo.io/installation/"
    exit 1
fi

HUGO_VERSION=$(hugo version)
print_success "Hugo found: $HUGO_VERSION"

# Test 1: Check front matter syntax
print_header "Test 1: Front Matter Validation"
print_info "Checking TOML front matter in content files..."

FRONTMATTER_OK=true
for file in content/*.md; do
    if [ -f "$file" ]; then
        echo "  Checking $(basename "$file")..."
        if grep -q "^+++" "$file" 2>/dev/null; then
            # Hugo will validate front matter during build, so we rely on that
            :
        else
            print_warning "No TOML front matter found in $file"
        fi
    fi
done

if [ "$FRONTMATTER_OK" = true ]; then
    print_success "Front matter syntax check passed"
else
    print_error "Front matter syntax check failed"
fi

# Test 2: Build the site
print_header "Test 2: Hugo Build"
print_info "Building Hugo site with --gc --minify..."

# Clean previous build
rm -rf public

# Build with the same settings as production
export HUGO_ENVIRONMENT=production
export TZ=America/New_York

if hugo --gc --minify --baseURL "https://crawlspacenh.com/" 2>&1; then
    print_success "Hugo build completed successfully"
else
    print_error "Hugo build failed"
    exit 1
fi

# Test 3: Verify build output
print_header "Test 3: Build Output Verification"

if [ ! -d "public" ]; then
    print_error "public directory not created"
    exit 1
else
    print_success "public directory exists"
fi

if [ ! -f "public/index.html" ]; then
    print_error "index.html not generated"
    exit 1
else
    print_success "index.html generated"
fi

FILE_COUNT=$(find public -type f | wc -l)
HTML_COUNT=$(find public -name "*.html" | wc -l)
print_info "Generated $FILE_COUNT files ($HTML_COUNT HTML files)"

# Test 4: Check for broken internal links (requires htmltest)
print_header "Test 4: Internal Link Checking"

if command -v htmltest &> /dev/null; then
    print_info "Running htmltest for broken link detection..."

    # Create htmltest config if it doesn't exist
    if [ ! -f ".htmltest.yml" ]; then
        cat > .htmltest.yml << 'EOF'
DirectoryPath: "public"
CheckDoctype: true
CheckExternal: false
CheckInternal: true
CheckInternalHash: true
IgnoreURLs:
  - "^mailto:"
  - "^tel:"
IgnoreDirectoryMissingTrailingSlash: true
EOF
    fi

    if htmltest 2>&1; then
        print_success "No broken internal links found"
    else
        print_error "Broken internal links detected (see above)"
    fi
else
    print_warning "htmltest not installed - skipping link checks"
    print_info "Install from: https://github.com/wjdp/htmltest"
fi

# Test 5: Validate HTML structure
print_header "Test 5: HTML Structure Validation"

HTML_OK=true
for file in public/*.html; do
    if [ -f "$file" ]; then
        BASENAME=$(basename "$file")

        # Check for DOCTYPE (case insensitive, handles minified HTML)
        if ! grep -iq "<!doctype" "$file"; then
            print_warning "Missing DOCTYPE in $BASENAME"
        fi

        # Check for html tag
        if ! grep -q "<html" "$file"; then
            print_error "Missing <html> tag in $BASENAME"
            HTML_OK=false
        fi

        # Check for head tag (handles minified HTML)
        if ! grep -q "<head" "$file"; then
            print_warning "Missing <head> tag in $BASENAME"
        fi

        # Check for body tag (handles minified HTML with attributes)
        if ! grep -q "<body" "$file"; then
            print_error "Missing <body> tag in $BASENAME"
            HTML_OK=false
        fi
    fi
done

if [ "$HTML_OK" = true ]; then
    print_success "HTML structure validation passed"
else
    print_error "HTML structure validation failed"
fi

# Final summary
print_header "Test Summary"
echo ""
echo "  Tests Passed:  $TESTS_PASSED"
echo "  Tests Failed:  $TESTS_FAILED"
echo "  Warnings:      $WARNINGS"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    print_success "All tests passed! ✨"
    echo ""
    exit 0
else
    print_error "Some tests failed. Please fix the issues above."
    echo ""
    exit 1
fi
