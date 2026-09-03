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

BuildRequires: cargo
BuildRequires: rust
BuildRequires: openssl-devel

%description
%{summary}

%prep
%autosetup -n %{name}-%{version}
# Cargo.toml pins ansi-to-tui to a commit in the Cretezy/ansi-to-tui git
# repo, which no longer exists (the project was transferred to the
# ratatui org and is now published to crates.io, still under the "7"
# major lazyjj's Cargo.toml constrains it to). Repoint the dependency at
# crates.io, then re-lock just that one package with the network-enabled
# `cargo update -p`: this asks cargo to compute the new source/checksum
# for ansi-to-tui itself against whatever's current on crates.io today,
# rather than this spec hardcoding a specific version/checksum that
# would silently go stale. Every other entry in the upstream-shipped
# Cargo.lock is left untouched (unlike `cargo generate-lockfile`, which
# would re-resolve the whole graph to newest-compatible and drift from
# what upstream actually tested).
sed -i 's|ansi-to-tui = { git = "https://github.com/Cretezy/ansi-to-tui.git", rev = "74bd97e" }|ansi-to-tui = "7"|' Cargo.toml
cargo update -p ansi-to-tui

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
