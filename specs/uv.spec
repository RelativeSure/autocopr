%global debug_package %{nil}

Name:    uv
Version: 0.7.12
Release: 1%{?dist}
Summary: An extremely fast Python package and project manager, written in Rust.

License:    MIT
URL:        https://github.com/astral-sh/uv
Source:     %{url}/releases/download/%{version}/%{name}-x86_64-unknown-linux-musl.tar.gz
Source1:    https://raw.githubusercontent.com/astral-sh/uv/%{version}/README.md
Source2:    https://raw.githubusercontent.com/astral-sh/uv/main/LICENSE-MIT

%description
Highlights
🚀 A single tool to replace pip, pip-tools, pipx, poetry, pyenv, twine, virtualenv, and more.
⚡️ 10-100x faster than pip.
🐍 Installs and manages Python versions.
🛠️ Runs and installs Python applications.
❇️ Runs scripts, with support for inline dependency metadata.
🗂️ Provides comprehensive project management, with a universal lockfile.
🔩 Includes a pip-compatible interface for a performance boost with a familiar CLI.
🏢 Supports Cargo-style workspaces for scalable projects.
💾 Disk-space efficient, with a global cache for dependency deduplication.
⏬ Installable without Rust or Python via curl or pip.
🖥️ Supports macOS, Linux, and Windows.
uv is backed by Astral, the creators of Ruff.

%prep
%autosetup -c -n %{name}

cp %{SOURCE1} CONFIGURATION.md
cp %{SOURCE2} LICENSE

%build

%install
# Ensure the source binary is in the expected location
install -p -D %{name}-x86_64-unknown-linux-musl/%{name} %{buildroot}%{_bindir}/%{name}
install -D -m 0644 CONFIGURATION.md %{buildroot}%{_docdir}/%{name}/README.md
install -D -m 0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%files
%doc %{_docdir}/%{name}/README.md
%license %{_datadir}/licenses/%{name}/LICENSE
%{_bindir}/%{name}
