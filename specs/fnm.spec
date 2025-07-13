%global debug_package %{nil}

Name:    fnm
Version: 1.38.1
Release: 1%{?dist}
Summary: Fast and simple Node.js version manager, built in Rust

License: GPL-3.0-or-later
URL:     https://github.com/Schniz/fnm
Source0: %{url}/archive/refs/tags/v%{version}.tar.gz
Source1: https://raw.githubusercontent.com/Schniz/fnm/v%{version}/LICENSE

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
cp %{SOURCE1} LICENSE
%if 0%{?el8}
  curl https://sh.rustup.rs -sSf | sh -s -- --profile minimal -y
%endif


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

install -D -m 0644 README.md %{buildroot}%{_docdir}/%{name}/README.md
install -D -m 0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%files
%license %{_datadir}/licenses/%{name}/LICENSE
%doc %{_docdir}/%{name}/README.md
%{_bindir}/%{name}
