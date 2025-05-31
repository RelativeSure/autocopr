%global debug_package %{nil}

Name:    atuin
Version: 18.6.1
Release: 1%{?dist}
Summary: Magical shell history

License:    MIT
URL:        https://github.com/atuinsh/atuin
Source:     %{url}/releases/download/v%{version}/%{name}-x86_64-unknown-linux-musl.tar.gz
Source1:    https://raw.githubusercontent.com/atuinsh/atuin/v%{version}/README.md
Source2:    https://raw.githubusercontent.com/atuinsh/atuin/v%{version}/CHANGELOG.md
Source3:    https://raw.githubusercontent.com/atuinsh/atuin/v%{version}/LICENSE

BuildRequires: glibc
BuildRequires: gcc
BuildRequires: python3-kobo-rpmlib

%description
Atuin replaces your existing shell history with a SQLite database, and records additional context for your commands.
Additionally, it provides optional and fully encrypted synchronization of your history between machines, via an Atuin server.

%prep
%autosetup -c
cp %{SOURCE1} CONFIGURATION.md
cp %{SOURCE2} .
cp %{SOURCE3} .

%build

%install
# Ensure the source binary is in the expected location
install -p -D %{name}-x86_64-unknown-linux-musl/%{name} %{buildroot}%{_bindir}/%{name}
install -D -m 0644 CONFIGURATION.md %{buildroot}%{_docdir}/%{name}/README.md
install -D -m 0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%files
%doc %{_docdir}/%{name}/README.md
%doc CHANGELOG.md
%license %{_datadir}/licenses/%{name}/LICENSE
%{_bindir}/%{name}
