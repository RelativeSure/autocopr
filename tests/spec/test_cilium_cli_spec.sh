#!/bin/bash
set -euo pipefail

# Test script for cilium-cli.spec file
# Testing framework: Shell scripting with rpmlint and rpmspec validation

SPEC_FILE="specs/cilium-cli.spec"
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test helper function
run_test() {
    local test_name="$1"
    local test_command="$2"
    ((TEST_COUNT++))

    echo -e "${YELLOW}Running test: $test_name${NC}"

    if eval "$test_command"; then
        echo -e "${GREEN}✓ PASS: $test_name${NC}"
        ((PASS_COUNT++))
    else
        echo -e "${RED}✗ FAIL: $test_name${NC}"
        ((FAIL_COUNT++))
    fi
}

# Ensure spec file exists
if [[ ! -f "$SPEC_FILE" ]]; then
    echo -e "${RED}Error: Spec file $SPEC_FILE not found${NC}"
    exit 1
fi

# --- Syntax and lint validation ---
run_test "Spec file syntax validation" \
    "rpmspec --parse '$SPEC_FILE' > /dev/null 2>&1"

run_test "RPMLint validation" \
    "command -v rpmlint > /dev/null && rpmlint '$SPEC_FILE' || echo 'rpmlint not available, skipping'"

# --- Metadata validation ---
run_test "Name field validation" \
    "grep -q '^Name:[[:space:]]*cilium-cli' '$SPEC_FILE'"

run_test "Version field validation" \
    "grep -q '^Version:[[:space:]]*[0-9]\\+\\.[0-9]\\+\\.[0-9]\\+' '$SPEC_FILE'"

run_test "Release field validation" \
    "grep -q '^Release:[[:space:]]*[0-9]\\+%{?dist}' '$SPEC_FILE'"

run_test "Summary field validation" \
    "grep -q '^Summary:.*CLI.*install.*manage.*troubleshoot' '$SPEC_FILE'"

run_test "License field validation" \
    "grep -q '^License:[[:space:]]*Apache-2.0' '$SPEC_FILE'"

run_test "URL field validation" \
    "grep -q '^URL:.*https://github.com/cilium/cilium-cli' '$SPEC_FILE'"

run_test "Source0 field validation" \
    "grep -q '^Source0:.*github.com/cilium/cilium-cli.*%{version}' '$SPEC_FILE'"

# --- Build requirements ---
run_test "Golang build requirement validation" \
    "grep -q '^BuildRequires:.*golang.*1.20' '$SPEC_FILE'"

run_test "Git build requirement validation" \
    "grep -q '^BuildRequires:.*git' '$SPEC_FILE'"

# --- Description section ---
run_test "Description section exists" \
    "grep -q '^%description' '$SPEC_FILE'"

run_test "Description content validation" \
    "sed -n '/^%description/,/^%prep/p' '$SPEC_FILE' | grep -q 'CLI.*install.*manage.*troubleshoot.*Kubernetes.*Cilium'"

# --- Debug package ---
run_test "Debug package disabled" \
    "grep -q '^%global debug_package %{nil}' '$SPEC_FILE'"

# --- Build section ---
run_test "Build section exists" \
    "grep -q '^%build' '$SPEC_FILE'"

run_test "Go build command validation" \
    "grep -A 10 '^%build' '$SPEC_FILE' | grep -q 'go build'"

run_test "Build flags validation" \
    "grep -A 10 '^%build' '$SPEC_FILE' | grep -q '\\-trimpath.*\\-buildmode=pie.*\\-mod=readonly'"

run_test "Version ldflags validation" \
    "grep -A 10 '^%build' '$SPEC_FILE' | grep -q '\\-ldflags.*Version=%{version}'"

# --- Install section ---
run_test "Install section exists" \
    "grep -q '^%install' '$SPEC_FILE'"

run_test "Binary installation validation" \
    "grep -A 5 '^%install' '$SPEC_FILE' | grep -q 'install.*cilium.*%{buildroot}%{_bindir}/cilium'"

run_test "License installation validation" \
    "grep -A 5 '^%install' '$SPEC_FILE' | grep -q 'install.*LICENSE.*%{_datadir}/licenses'"

# --- Verify script ---
run_test "Verify script exists" \
    "grep -q '^%verifyscript' '$SPEC_FILE'"

run_test "Verify script command validation" \
    "grep -A 2 '^%verifyscript' '$SPEC_FILE' | grep -q 'cilium version'"

# --- Files section ---
run_test "Files section exists" \
    "grep -q '^%files' '$SPEC_FILE'"

run_test "Binary file packaging validation" \
    "grep -A 5 '^%files' '$SPEC_FILE' | grep -q '%{_bindir}/cilium'"

run_test "License file packaging validation" \
    "grep -A 5 '^%files' '$SPEC_FILE' | grep -q '%license.*%{_datadir}/licenses/%{name}/LICENSE'"

# --- Changelog ---
run_test "Changelog section exists" \
    "grep -q '^%changelog' '$SPEC_FILE'"

run_test "Autochangelog usage validation" \
    "grep -A 2 '^%changelog' '$SPEC_FILE' | grep -q '%autochangelog'"

# --- Environment variables in build section ---
run_test "CGO environment variables validation" \
    "grep -A 10 '^%build' '$SPEC_FILE' | grep -q 'export CGO_CPPFLAGS.*CGO_CFLAGS.*CGO_CXXFLAGS.*CGO_LDFLAGS'"

# --- Edge case tests ---
run_test "No duplicate Name fields" \
    "[[ \$(grep -c '^Name:' '$SPEC_FILE') -eq 1 ]]"

run_test "No duplicate Version fields" \
    "[[ \$(grep -c '^Version:' '$SPEC_FILE') -eq 1 ]]"

run_test "No duplicate License fields" \
    "[[ \$(grep -c '^License:' '$SPEC_FILE') -eq 1 ]]"

run_test "Version format compliance" \
    "grep -q '^Version:' '$SPEC_FILE' | grep -q '[0-9]\\+\\.[0-9]\\+\\.[0-9]\\+'"

run_test "No hardcoded paths in build section" \
    "! grep -A 10 '^%build' '$SPEC_FILE' | grep -q '/usr/local\\|/opt'"

run_test "Proper macro usage for directories" \
    "grep '%{_bindir}\\|%{_datadir}' '$SPEC_FILE' > /dev/null"

# --- Security and best practices ---
run_test "No world-writable permissions" \
    "! grep 'install.*-m.*7' '$SPEC_FILE'"

run_test "Binary has executable permissions" \
    "grep 'install.*cilium.*0755' '$SPEC_FILE' > /dev/null"

run_test "License file has correct permissions" \
    "grep 'install.*LICENSE.*0644' '$SPEC_FILE' > /dev/null"

# --- Prep section ---
run_test "Prep section exists" \
    "grep -q '^%prep' '$SPEC_FILE'"

run_test "Autosetup macro usage" \
    "grep -A 2 '^%prep' '$SPEC_FILE' | grep -q '%autosetup.*cilium-cli-%{version}'"

# --- Test summary and exit ---
echo -e "\n${YELLOW}=== Test Summary ===${NC}"
echo "Total tests: $TEST_COUNT"
echo -e "${GREEN}Passed: $PASS_COUNT${NC}"
echo -e "${RED}Failed: $FAIL_COUNT${NC}"

if [[ $FAIL_COUNT -eq 0 ]]; then
    echo -e "\n${GREEN}All tests passed! ✓${NC}"
    exit 0
else
    echo -e "\n${RED}Some tests failed! ✗${NC}"
    exit 1
fi