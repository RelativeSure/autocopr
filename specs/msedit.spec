%global debug_package %{nil}

Name:    msedit
Version: 1.2.0
Release: 1%{?dist}
Summary: A simple editor for simple needs.

License: MIT
URL:     https://github.com/microsoft/edit
Source0: %{url}/archive/v%{version}.tar.gz

# Standard Rust build dependencies
BuildRequires: rust >= 1.70
BuildRequires: cargo >= 1.70
# Added openssl-devel as it's a common implicit dependency for Rust networking crates
# and might be needed by some underlying dependency of 'edit'.
BuildRequires: openssl-devel
# Added pkg-config for build scripts that need to find C libraries
BuildRequires: pkg-config


%description
A simple editor for simple needs. Pays homage to the classic MS-DOS Editor,
but with a modern interface and input controls similar to VS Code. The goal
is to provide an accessible editor that even users largely unfamiliar with
terminals can easily use.

%prep
%autosetup -n edit-%{version}

%build
# Set RUSTC_BOOTSTRAP=1 to enable usage of nightly features,
# as per upstream build instructions.
export RUSTC_BOOTSTRAP=1
# Ensure correct environment flags are passed to cargo
export CARGO_TERM_COLOR=always
cargo build --config .cargo/release.toml --release --verbose

%install
rm -rf %{buildroot}
install -D -m 0755 target/release/edit %{buildroot}%{_bindir}/msedit
install -D -m 0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%files
%{_bindir}/msedit
%license %{_datadir}/licenses/%{name}/LICENSE
