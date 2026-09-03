%global debug_package %{nil}

Name:    lucky-commit
Version: 2.2.5
Release: 1%{?dist}
Summary: Customize your git commit hashes

License: MIT
URL:     https://github.com/not-an-aardvark/lucky-commit
Source0: %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust
BuildRequires: git

%description
%{summary}.

%prep
%autosetup -n %{name}-%{version}

%build
# Default build links against OpenCL to run on a GPU; COPR builders have
# neither a GPU nor an OpenCL runtime, so build the portable, upstream-
# documented CPU-only fallback instead (--no-default-features).
cargo build --release --no-default-features --locked

%install
cargo install --path . --root %{buildroot} --no-default-features --locked
install -Dm0755 %{buildroot}/bin/lucky_commit %{buildroot}%{_bindir}/lucky_commit
rm -f %{buildroot}/bin/lucky_commit
rm -f %{buildroot}/.crates.toml %{buildroot}/.crates2.json

%check
# lucky_commit has no --version, and --help/-h exits non-zero by design;
# running with no args operates on the current git repo's HEAD commit,
# which doesn't exist in the build sandbox. Just confirm the binary is
# present and executable instead of invoking it.
test -x %{buildroot}%{_bindir}/lucky_commit

%files
%{_bindir}/lucky_commit
%license LICENSE.md
%doc README.md

%changelog
%autochangelog
