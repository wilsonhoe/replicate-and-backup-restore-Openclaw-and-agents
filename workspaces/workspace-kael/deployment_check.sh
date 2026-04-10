#!/bin/bash
set -euo pipefail

# Colors
readonly RED=$'\e[31m'
readonly GREEN=$'\e[32m'
readonly YELLOW=$'\e[33m'
readonly BLUE=$'\e[34m'
readonly NC=$'\e[0m'

success() { echo -e "${GREEN}✓ $1${NC}"; }
error() { echo -e "${RED}✗ $1${NC}"; exit 1; }
warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
section() { echo -e "\n${BLUE}=== $1 ===${NC}"; }

VERBOSE=${VERBOSE:-false}
SKIP_INTEGRATION=${SKIP_INTEGRATION:-false}

while [[ $# -gt 0 ]]; do
  case $1 in
    --verbose) VERBOSE=true; shift ;;
    --skip-integration) SKIP_INTEGRATION=true; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

passed=0
total_checks=0

check() {
  local desc="$1"
  shift
  total_checks=$((total_checks + 1))
  if "$@"; then
    success "$desc"
    passed=$((passed + 1))
  else
    error "$desc"
  fi
}

section "1. Environment Checks"

# Env vars from .env.example
if [[ -f .env.example ]]; then
  missing=()
  while IFS='=' read -r key _; do
    key=$(echo "$key" | xargs) # trim
    [[ $key =~ ^[[:space:]]*#|^[[:space:]]*$ ]] && continue
    [[ -n "${!key:-}" ]] || missing+=("$key")
  done < .env.example
  ((${#missing[@]} == 0)) || error "Missing env vars: ${missing[*]}"
  success "All env vars set"
else
  warning ".env.example not found, skipping"
fi

# Node version
if [[ -f .nvmrc ]]; then
  required=$(tr -d ' \n\r' < .nvmrc)
  current=$(node --version | sed 's/^v//; s/ .*//')
  [[ "$current" == "$required"* ]] || error "Node version mismatch: $current != $required*"
  success "Node version OK"
fi

# Disk space >1GB (in KB)
avail_kb=$(df --output=avail -k . | tail -1)
(( avail_kb > 1048576 )) || error "Disk space <1GB ($avail_kb KB)"
success "Disk space OK"

# Memory >512MB available
avail_kb=$(free | awk '/Mem:/ {print $7}')
(( avail_kb > 524288 )) || error "Memory <512MB ($avail_kb KB)"
success "Memory OK"

section "2. Code Quality"

check "Lint" npm run lint
check "Type check" npx tsc --noEmit

# No TODO/FIXME in changed files
git fetch origin >/dev/null 2>&1 || git fetch >/dev/null 2>&1
changed=$(git diff --name-only origin/main..HEAD | grep -E '\.(js?|jsx?|ts?|tsx?)$' || true)
if [[ -n "$changed" ]]; then
  grep -i -l -H 'todo\|fixme' $changed | grep . && error "TODO/FIXME in changed files" || success "No TODO/FIXME"
else
  success "No changed files"
fi

section "3. Test Suite"

check "Unit tests" npm test
if [[ $SKIP_INTEGRATION == false ]]; then
  check "Integration tests" npm run test:integration
fi

# Coverage >80%
if command -v nyc >/dev/null 2>&1 || grep -q coverage package.json; then
  coverage=$(npm test -- --coverage | tail -5 | grep -o '[0-9]\+%' | head -1 | sed 's/%//')
  (( coverage >= 80 )) || error "Coverage $coverage% <80%"
  success "Test coverage $coverage%"
else
  warning "No coverage tool found"
fi

section "4. Security"

# npm audit
high_crit=$(npm audit --json 2>/dev/null | jq '.metadata.vulnerabilities.high // 0 + .metadata.vulnerabilities.critical // 0' || echo 0)
(( high_crit == 0 )) || error "$high_crit high/critical vulns in npm audit"
success "npm audit clean"

# Hardcoded secrets (basic scan)
grep -rEil '(aws[_-]?)?[A-Z0-9]{20}|[a-z]+[_-]?key|pass(wd|word)|secret' src/ --exclude-dir={node_modules,coverage,dist} | grep -v -E '(test|example|dummy|placeholder)' | grep . && error "Potential secrets found" || success "No hardcoded secrets"

# .env excluded
grep -q '^\.env' .gitignore 2>/dev/null || error ".env not in .gitignore"
success ".env excluded"

section "5. Build"

rm -rf dist build .next
check "Build" npm run build
[[ -n "$(find . -maxdepth 1 -name 'dist' -o -name 'build' -o -name '.next' -type d 2>/dev/null)" ]] || error "Build artifacts missing"
success "Build successful"

section "6. Database"

if command -v npx >/dev/null 2>&1 && grep -q prisma package.json 2>/dev/null; then
  pending=$(npx prisma migrate status 2>/dev/null | grep 'Pending' | wc -l)
  (( pending == 0 )) || error "$pending pending migrations"
  success "No pending migrations"

  # Sequential migrations
  if [[ -d prisma/migrations ]]; then
    mapfile -t migs < <(ls -1v prisma/migrations/)
    for i in "${!migs[@]}"; do
      [[ "${migs[i]}" =~ [0-9]{14}_[0-9]+ ]] || { error "Non-standard migration name: ${migs[i]}"; exit 1; }
      num=$(echo "${migs[i]}" | sed 's/^..............\([0-9]\+\).*/\1/')
      (( num == i + 1 )) || { error "Migration gap at $((i+1)): ${migs[i]}"; exit 1; }
    done
    success "Migrations sequential"
  fi
else
  warning "No Prisma detected"
fi

echo -e "\n${BLUE}=== SUMMARY ===${NC}"
echo "Passed: $passed / $total_checks"
(( passed == total_checks )) && { success "All checks passed! Ready to deploy."; exit 0; }
error "Deployment blocked."
