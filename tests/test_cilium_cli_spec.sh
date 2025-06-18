#!/bin/bash
# Comprehensive test suite for cilium-cli.spec file
# Tests spec file syntax, build requirements, and package validation

set -euo pipefail

SPEC_FILE="specs/cilium-cli.spec"
TEST_DIR="$(dirname "$0")"
TEMP_DIR=$(mktemp -d)
FAILED_TESTS=0
TOTAL_TESTS=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test result tracking
run_test() {
    local test_name="$1"
    local test_command="$2"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    echo -e "${YELLOW}Running: $test_name${NC}"
    if eval "$test_command"; then
        echo -e "${GREEN}✓ PASS: $test_name${NC}"
    else
        echo -e "${RED}✗ FAIL: $test_name${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    echo
}

cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Test 1: Check if spec file exists and is readable
test_spec_file_exists() {
    [[ -f "$SPEC_FILE" && -r "$SPEC_FILE" ]]
}

# Test 2: Validate spec file syntax using rpmspec
test_spec_syntax_validation() {
    if command -v rpmspec >/dev/null 2>&1; then
        rpmspec -P "$SPEC_FILE" >/dev/null 2>&1
    else
        echo "rpmspec not available, skipping syntax validation"
        return 0
    fi
}

# Test 3: Check for required RPM spec fields
test_required_fields() {
    local required_fields=("Name:" "Version:" "Release:" "Summary:" "License:" "URL:" "Source0:")
    for field in "${required_fields[@]}"; do
        if ! grep -q "^$field" "$SPEC_FILE"; then
            echo "Missing required field: $field"
            return 1
        fi
    done
}

# Test 4: Validate version format
test_version_format() {
    local version
    version=$(grep "^Version:" "$SPEC_FILE" | awk '{print $2}')
    if [[ ! "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "Invalid version format: $version"
        return 1
    fi
}

# Test 5: Check license field validity
test_license_validity() {
    local license
    license=$(grep "^License:" "$SPEC_FILE" | cut -d' ' -f2-)
    local valid_licenses=("Apache-2.0" "MIT" "GPL-2.0" "GPL-3.0" "BSD-3-Clause")
    local found=false
    for valid in "${valid_licenses[@]}"; do
        if [[ "$license" == *"$valid"* ]]; then
            found=true
            break
        fi
    done
    if [[ "$found" == false ]]; then
        echo "License '$license' should be a valid SPDX identifier"
        return 1
    fi
}

# Test 6: Validate BuildRequires dependencies
test_build_requirements() {
    if ! grep -q "BuildRequires:.*golang" "$SPEC_FILE"; then
        echo "Missing golang BuildRequires"
        return 1
    fi
    if ! grep -q "BuildRequires:.*git" "$SPEC_FILE"; then
        echo "Missing git BuildRequires"
        return 1
    fi
}

# Test 7: Check golang version requirement
test_golang_version_requirement() {
    local golang_req version major minor
    golang_req=$(grep "BuildRequires:.*golang" "$SPEC_FILE")
    if [[ "$golang_req" == *">="* ]]; then
        version=$(echo "$golang_req" | grep -oE '[0-9]+\.[0-9]+')
        major=${version%%.*}
        minor=${version##*.}
        if (( major < 1 || minor < 20 )); then
            echo "Golang version requirement should be >= 1.20"
            return 1
        fi
    fi
}

# Test 8: Validate Source0 URL format
test_source_url_format() {
    local source_url
    source_url=$(grep "^Source0:" "$SPEC_FILE" | awk '{print $2}')
    if [[ ! "$source_url" =~ ^https:// ]]; then
        echo "Source0 URL should use HTTPS"
        return 1
    fi
    if [[ ! "$source_url" == *".tar.gz" ]]; then
        echo "Source0 should point to a tar.gz archive"
        return 1
    fi
}

# Test 9: Check for security-related build flags
test_security_build_flags() {
    if ! grep -q "trimpath" "$SPEC_FILE"; then
        echo "Build should include -trimpath flag for security"
        return 1
    fi
    if ! grep -q "buildmode=pie" "$SPEC_FILE"; then
        echo "Build should include -buildmode=pie for security"
        return 1
    fi
}

# Test 10: Validate %files section
test_files_section() {
    if ! grep -q "%{_bindir}/cilium" "$SPEC_FILE"; then
        echo "Missing binary file in %files section"
        return 1
    fi
    if ! grep -q "%license.*LICENSE" "$SPEC_FILE"; then
        echo "Missing license file in %files section"
        return 1
    fi
}

# Test 11: Check install section commands
test_install_section() {
    if ! grep -q "install.*cilium.*%{buildroot}%{_bindir}" "$SPEC_FILE"; then
        echo "Missing binary installation command"
        return 1
    fi
    if ! grep -q "install.*LICENSE.*%{buildroot}" "$SPEC_FILE"; then
        echo "Missing license installation command"
        return 1
    fi
}

# Test 12: Validate verifyscript functionality
test_verifyscript() {
    if ! grep -q "%verifyscript" "$SPEC_FILE"; then
        echo "Missing %verifyscript section"
        return 1
    fi
    if ! grep -q "%{buildroot}%{_bindir}/cilium version" "$SPEC_FILE"; then
        echo "Verifyscript should test cilium version command"
        return 1
    fi
}

# Test 13: Check for proper cleanup in %install
test_install_cleanup() {
    if ! grep -q "rm -rf %{buildroot}" "$SPEC_FILE"; then
        echo "Missing buildroot cleanup in %install section"
        return 1
    fi
}

# Test 14: Validate file permissions
test_file_permissions() {
    if ! grep -q "install.*-m 0755.*cilium" "$SPEC_FILE"; then
        echo "Binary should be installed with 0755 permissions"
        return 1
    fi
    if ! grep -q "install.*-m 0644.*LICENSE" "$SPEC_FILE"; then
        echo "License should be installed with 0644 permissions"
        return 1
    fi
}

# Test 15: Check for debug package disabling
test_debug_package_disabled() {
    if ! grep -q "%global debug_package %{nil}" "$SPEC_FILE"; then
        echo "Debug package should be explicitly disabled for Go binaries"
        return 1
    fi
}

# Test 16: Validate changelog section
test_changelog_section() {
    if ! grep -q "%changelog" "$SPEC_FILE"; then
        echo "Missing %changelog section"
        return 1
    fi
    if ! grep -q "%autochangelog" "$SPEC_FILE"; then
        echo "Should use %autochangelog for automatic changelog generation"
        return 1
    fi
}

# Test 17: Check for proper macro usage
test_macro_usage() {
    # Check for consistent use of RPM macros
    if grep -q "/usr/bin" "$SPEC_FILE" && ! grep -q "%{_bindir}" "$SPEC_FILE"; then
        echo "Should use %{_bindir} macro instead of hardcoded /usr/bin"
        return 1
    fi
}

# Test 18: Validate build environment variables
test_build_environment() {
    local env_vars=("CGO_CPPFLAGS" "CGO_CFLAGS" "CGO_CXXFLAGS" "CGO_LDFLAGS")
    for var in "${env_vars[@]}"; do
        if ! grep -q "export $var" "$SPEC_FILE"; then
            echo "Missing environment variable: $var"
            return 1
        fi
    done
}

# Test 19: Check ldflags for version information
test_version_ldflags() {
    if ! grep -q "ldflags.*Version=%{version}" "$SPEC_FILE"; then
        echo "Build should include version information in ldflags"
        return 1
    fi
}

# Test 20: Validate Go build flags
test_go_build_flags() {
    local required_flags=("-mod=readonly" "-modcacherw" "-linkmode=external")
    for flag in "${required_flags[@]}"; do
        if ! grep -q "$flag" "$SPEC_FILE"; then
            echo "Missing required Go build flag: $flag"
            return 1
        fi
    done
}

# Test execution function
run_all_tests() {
    echo "Starting cilium-cli.spec validation tests..."
    echo "=========================================="

    run_test "Spec file exists and is readable" "test_spec_file_exists"
    run_test "Spec file syntax validation" "test_spec_syntax_validation"
    run_test "Required fields present" "test_required_fields"
    run_test "Version format validation" "test_version_format"
    run_test "License validity check" "test_license_validity"
    run_test "Build requirements validation" "test_build_requirements"
    run_test "Golang version requirement" "test_golang_version_requirement"
    run_test "Source URL format validation" "test_source_url_format"
    run_test "Security build flags check" "test_security_build_flags"
    run_test "Files section validation" "test_files_section"
    run_test "Install section validation" "test_install_section"
    run_test "Verifyscript validation" "test_verifyscript"
    run_test "Install cleanup check" "test_install_cleanup"
    run_test "File permissions validation" "test_file_permissions"
    run_test "Debug package disabled check" "test_debug_package_disabled"
    run_test "Changelog section validation" "test_changelog_section"
    run_test "RPM macro usage validation" "test_macro_usage"
    run_test "Build environment validation" "test_build_environment"
    run_test "Version ldflags validation" "test_version_ldflags"
    run_test "Go build flags validation" "test_go_build_flags"

    echo "=========================================="
    echo "Test Summary:"
    echo "Total tests: $TOTAL_TESTS"
    echo "Failed tests: $FAILED_TESTS"
    echo "Passed tests: $((TOTAL_TESTS - FAILED_TESTS))"

    if [[ $FAILED_TESTS -eq 0 ]]; then
        echo -e "${GREEN}All tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}$FAILED_TESTS test(s) failed.${NC}"
        exit 1
    fi
}

# Additional utility function for manual spec file testing
test_rpmlint() {
    echo "Running rpmlint validation (if available)..."
    if command -v rpmlint >/dev/null 2>&1; then
        rpmlint "$SPEC_FILE" || echo "rpmlint found issues (may not be critical)"
    else
        echo "rpmlint not available, skipping"
    fi
}

# Main execution
main() {
    if [[ "${1:-}" == "--rpmlint" ]]; then
        test_rpmlint
    else
        run_all_tests
    fi
}

# Run tests if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi