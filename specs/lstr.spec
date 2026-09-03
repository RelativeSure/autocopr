%global debug_package %{nil}

Name: lstr
Version: 0.4.0
Release: 1%{?dist}
Summary: A fast, minimalist directory tree viewer, written in Rust

License: MIT
URL: https://github.com/bgreenwell/lstr
Source0: %{url}/archive/v%{version}/%{name}-v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: git

%description
%{summary}

%prep
%autosetup -n %{name}-%{version}

%build
cargo build --release

%install
cargo install --path . --root %{buildroot}
install -Dm0755 %{buildroot}/bin/lstr %{buildroot}%{_bindir}/lstr
rm -f %{buildroot}/bin/lstr
rm -f %{buildroot}/.crates.toml %{buildroot}/.crates2.json

%check
cargo test --release

%files
%{_bindir}/lstr
%license LICENSE
%doc README.md

%changelog
%autochangelog
