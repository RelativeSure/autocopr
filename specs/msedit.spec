%global debug_package %{nil}

Name:    msedit
Version: 1.2.0
Release: 1%{?dist}
Summary: A simple editor for simple needs.

License: MIT
URL:     https://github.com/microsoft/edit
Source0: %{url}/archive/v%{version}.tar.gz

BuildRequires: rust >= 1.70
BuildRequires: cargo >= 1.70
BuildRequires: rust-toolchain-nightly

%description
A simple editor for simple needs. Pays homage to the classic MS-DOS Editor,
but with a modern interface and input controls similar to VS Code. The goal
is to provide an accessible editor that even users largely unfamiliar with
terminals can easily use.

%prep
%autosetup -n edit-%{version}

%build
# Set RUSTC_BOOTSTRAP=1 to use nightly features
export RUSTC_BOOTSTRAP=1
cargo build --config .cargo/release.toml --release

%install
rm -rf %{buildroot}
install -D -m 0755 target/release/edit %{buildroot}%{_bindir}/msedit
install -D -m 0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%files
%{_bindir}/msedit
%license %{_datadir}/licenses/%{name}/LICENSE
