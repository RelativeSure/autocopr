%global debug_package %{nil}

Name:    lucky-commit
Version: 2.2.3
Release: 1%{?dist}
Summary: Make your git commits lucky!

License:    MIT
# https://github.com/not-an-aardvark/lucky-commit/archive/refs/tags/v2.2.3.tar.gz
URL:        https://github.com/not-an-aardvark/lucky-commit
Source:     %{url}/archive/refs/tags/v%{version}.tar.gz
Source1: https://github.com/not-an-aardvark/lucky-commit/blob/v%{version}/README.md

BuildRequires: cargo
BuildRequires: rust

%description
lucky-commit amends your commit messages by adding a few characters of various types of whitespace, and keeps trying new messages until it finds a good hash.
By default, it will look for a commit hash starting with "0000000".

%prep
%autosetup -n %{name}

cp %{SOURCE1} CONFIGURATION.md

#%build
#cargo build --release

%install
# Ensure the source binary is in the expected location
#install -p -D %{name} %{buildroot}%{_bindir}/%{name}

export CARGO_PROFILE_RELEASE_BUILD_OVERRIDE_OPT_LEVEL=3
cargo install --root=%{buildroot}%

rm -f %{buildroot}%{_prefix}/.crates.toml \
    %{buildroot}%{_prefix}/.crates2.json
strip --strip-all %{buildroot}%{_bindir}/*

%files
%doc CONFIGURATION.md
%{_bindir}/%{name}