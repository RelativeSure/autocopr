%global debug_package %{nil}

Name:    uv
Version: 0.12.9
Release: 1%{?dist}
Summary: An extremely fast Python package and project manager, written in Rust

License:    MIT
URL:        https://github.com/astral-sh/uv
Source:     %{url}/releases/download/%{version}/%{name}-x86_64-unknown-linux-musl.tar.gz
Source1:    https://raw.githubusercontent.com/astral-sh/uv/%{version}/README.md

%description
uv is a single tool that replaces pip, pip-tools, pipx, poetry, pyenv,
twine, virtualenv, and more. It is 10-100x faster than pip, installs
and manages Python versions, and runs and installs Python applications.
It can run scripts with support for inline dependency metadata, and it
provides comprehensive project management with a universal lockfile.
It includes a pip-compatible interface for a performance boost with a
familiar CLI, supports Cargo-style workspaces for scalable projects,
and is disk-space efficient with a global cache for dependency
deduplication. It is installable without Rust or Python via curl or
pip, and supports macOS, Linux, and Windows. uv is backed by Astral,
the creators of Ruff.

%prep
%autosetup -c -n %{name}

cp %{SOURCE1} CONFIGURATION.md

%build

%install
# Ensure the source binaries are in the expected location
install -p -D %{name}-x86_64-unknown-linux-musl/%{name} %{buildroot}%{_bindir}/%{name}
install -p -D %{name}-x86_64-unknown-linux-musl/uvx %{buildroot}%{_bindir}/uvx

%files
%doc CONFIGURATION.md
%{_bindir}/%{name}
%{_bindir}/uvx

%check
%{buildroot}%{_bindir}/%{name} --version

%changelog
%autochangelog
