%global debug_package %{nil}

Name:    lazyjj
Version: 0.6.1
Release: 1%{?dist}
Summary: TUI for Jujutsu/jj

License: Apache-2.0
URL: https://github.com/Cretezy/lazyjj
# Upstream stopped publishing prebuilt release binaries starting at v0.6.0
# (both v0.6.0 and v0.6.1 ship zero release assets), so build from source
# instead of downloading a release tarball. See GitHub issue #440.
Source0: %{url}/archive/refs/tags/v%{version}.tar.gz
# Cargo.toml (still, as of v0.6.1) pins ansi-to-tui to a commit in the
# Cretezy/ansi-to-tui git repo, which no longer exists (the project was
# transferred to the ratatui org and is now published to crates.io). This
# is a vendored Cargo.lock with that one entry repointed at the matching
# crates.io release (7.0.0, the last major depending on ratatui ^0.29 same
# as lazyjj, before ansi-to-tui 8.x split onto the incompatible
# ratatui-core crate) via `cargo update -p ansi-to-tui --precise 7.0.0`
# after making the same Cargo.toml edit applied in %%prep below - every
# other dependency stays pinned exactly as upstream's own lockfile had it,
# so the build stays reproducible instead of re-resolving the whole graph.
Source1: %{name}-%{version}-Cargo.lock

BuildRequires: cargo
BuildRequires: rust
BuildRequires: openssl-devel

%description
%{summary}

%prep
%autosetup -n %{name}-%{version}
sed -i 's|ansi-to-tui = { git = "https://github.com/Cretezy/ansi-to-tui.git", rev = "74bd97e" }|ansi-to-tui = "7"|' Cargo.toml
cp %{SOURCE1} Cargo.lock

%build
cargo build --release --locked

%install
cargo install --path . --root %{buildroot} --locked
install -Dm0755 %{buildroot}/bin/%{name} %{buildroot}%{_bindir}/%{name}
rm -f %{buildroot}/bin/%{name}
rm -f %{buildroot}/.crates.toml %{buildroot}/.crates2.json

%check
%{buildroot}%{_bindir}/%{name} --version

%files
%{_bindir}/%{name}
%license LICENSE
%doc README.md

%changelog
%autochangelog
