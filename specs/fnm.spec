%global debug_package %{nil}

Name:    fnm
Version: 1.39.0
Release: 1%{?dist}
Summary: Fast and simple Node.js version manager, built in Rust

License: GPL-3.0-only
URL:     https://github.com/Schniz/fnm
Source0: %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires: cargo >= 1.40
BuildRequires: rust >= 1.40
BuildRequires: gcc
BuildRequires: python3-devel
BuildRequires: cmake
BuildRequires: openssl-devel
BuildRequires: perl-devel
BuildRequires: openssl-perl
BuildRequires: perl-FindBin
BuildRequires: perl-IPC-Cmd

%description
%{summary}

%prep
%autosetup -p1
%if 0%{?el8}
  curl https://sh.rustup.rs -sSf | sh -s -- --profile minimal -y
%endif


# cargo install both compiles and places the binary in one step; a separate
# cargo build here followed by --offline cargo install would re-resolve
# dependencies independently and can fail (e.g. on yanked crate versions
# that only surface without network access), so %%build is intentionally
# left empty rather than split into two cargo invocations.
%build

%install
export CARGO_PROFILE_RELEASE_BUILD_OVERRIDE_OPT_LEVEL=3
%if 0%{?el8}
  $HOME/.cargo/bin/cargo install --root=%{buildroot}%{_prefix} --path=.
%else
  cargo install --root=%{buildroot}%{_prefix} --path=.
%endif

rm -f %{buildroot}%{_prefix}/.crates.toml \
    %{buildroot}%{_prefix}/.crates2.json
strip --strip-all %{buildroot}%{_bindir}/*

%check
%{buildroot}%{_bindir}/%{name} --version

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%changelog
%autochangelog
