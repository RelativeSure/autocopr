%global debug_package %{nil}

Name: lstr
Version: 0.2.0
Release: 1%{?dist}
Summary: A fast, minimalist directory tree viewer, written in Rust.

License: MIT
URL: https://github.com/bgreenwell/lstr
Source0: %{url}/archive/v%{version}/%{name}-v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust
BuildRequires: openssl-devel

%description
%{summary}

%prep
%autosetup -n %{name}-%{version}

%build
cargo build --release

%install
cargo install --path . --root %{buildroot} --prefix %{_prefix}

%files
%{_bindir}/lstr
%doc README.md

%changelog
%autochangelog
