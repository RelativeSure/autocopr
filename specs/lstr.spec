%global debug_package %{nil}

Name: lstr
Version: 0.2.0
Release: 1%{?dist}
Summary: A fast, minimalist directory tree viewer, written in Rust.

License: MIT
URL: https://github.com/bgreenwell/lstr
Source0: %{url}/archive/v%{version}/%{name}-v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust
BuildRequires: clap_complete
BuildRequires: clap_mangen
BuildRequires: gzip

%description
%{summary}

%prep
%autosetup -n %{name}-v%{version}

%build
cargo build --release

# Generate completions
clap_complete lstr --bash > lstr.bash
clap_complete lstr --fish > lstr.fish
clap_complete lstr --zsh > _lstr

# Generate man page
clap_mangen lstr --outdir .
gzip lstr.1

%install
cargo install --path . --root %{buildroot} --prefix %{_prefix}

# Install completions
install -v -p -D -m 0644 lstr.bash %{buildroot}%{_datadir}/bash-completion/completions/lstr
install -v -p -D -m 0644 lstr.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/lstr.fish
install -v -p -D -m 0644 _lstr %{buildroot}%{_datadir}/zsh/site-functions/_lstr

# Install man page
install -pvD -m 0644 lstr.1.gz %{buildroot}%{_mandir}/man1/lstr.1.gz

%files
%{_bindir}/lstr
%doc README.md
%{_datadir}/bash-completion/completions/lstr
%{_datadir}/fish/vendor_completions.d/lstr.fish
%{_datadir}/zsh/site-functions/_lstr
%{_mandir}/man1/lstr.1.gz

%changelog
%autochangelog
