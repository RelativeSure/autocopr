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
# Cargo.toml pins ansi-to-tui to a commit in the Cretezy/ansi-to-tui git repo,
# which no longer exists (the project was transferred to the ratatui org and
# is now published to crates.io). Repoint the dependency at the matching
# crates.io release (7.x, the last major depending on ratatui ^0.29 same as
# lazyjj, before ansi-to-tui 8.x split onto the incompatible ratatui-core
# crate) so the build doesn't need to reach a dead git URL, and drop the
# stale lockfile entry so Cargo re-resolves it.
sed -i 's|ansi-to-tui = { git = "https://github.com/Cretezy/ansi-to-tui.git", rev = "74bd97e" }|ansi-to-tui = "7"|' Cargo.toml
rm -f Cargo.lock

%build
cargo build --release

%install
cargo install --path . --root %{buildroot}
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
