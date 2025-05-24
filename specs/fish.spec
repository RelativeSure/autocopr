%global debug_package %{nil}

Name:    fish
Version: 4.0.2
Release: 1%{?dist}
Summary: The user-friendly command line shell.

License: MIT
# https://github.com/fish-shell/fish-shell/releases/download/4.0.2/fish-4.0.2.tar.xz
URL:     https://github.com/fish-shell/fish-shell
Source:  %{url}/releases/download/%{version}/fish-%{version}.tar.xz
Source1: https://raw.githubusercontent.com/fish-shell/fish-shell/%{version}/README.rst
Source2: https://raw.githubusercontent.com/fish-shell/fish-shell/%{version}/COPYING

%description
Fish is a smart and user-friendly command line shell for Linux, macOS, and the rest
of the family. Fish includes features like syntax highlighting, autosuggestions,
and tab completions that just work, with nothing to learn or configure.

%prep
%autosetup -c
cp %{SOURCE1} README.md
cp %{SOURCE2} LICENSE

%install
ls -larth
ls -larth %{name}-%{version} || true
ls -larth %{name}-%{version}/* || true
ls -larth %{buildroot} || true
ls -larth %{buildroot}%{_bindir} || true

install -v -p -D %{name} %{buildroot}%{_bindir}/%{name}
install -v -p -D %{name}_indent %{buildroot}%{_bindir}/%{name}_indent
install -v -p -D %{name}_key_reader %{buildroot}%{_bindir}/%{name}_key_reader

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}_indent
%{_bindir}/%{name}_key_reader

%changelog
%autochangelog
