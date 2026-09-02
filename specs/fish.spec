%global debug_package %{nil}

Name:    fish
Version: 4.8.1
Release: 1%{?dist}
Summary: The user-friendly command line shell

License: MIT
URL:     https://github.com/fish-shell/fish-shell
Source:  %{url}/releases/download/%{version}/fish-%{version}.tar.xz
Source1: https://raw.githubusercontent.com/fish-shell/fish-shell/%{version}/README.rst
Source2: https://raw.githubusercontent.com/fish-shell/fish-shell/%{version}/COPYING

BuildRequires: cmake >= 3.19
BuildRequires: cargo >= 1.40
BuildRequires: rust >= 1.40
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: ncurses-devel
BuildRequires: pcre2-devel
BuildRequires: gettext-devel
BuildRequires: python3-sphinx

%description
Fish is a smart and user-friendly command line shell for Linux, macOS,
and the rest of the family. Fish includes features like syntax
highlighting, autosuggestions, and tab completions that just work,
with nothing to learn or configure.

This is a COPR-only build and intentionally shadows the official
Fedora fish package (src.fedoraproject.org/rpms/fish) for users of
this repo who want a newer release.


%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1} README.md
cp %{SOURCE2} LICENSE

%build
%cmake
%cmake_build

%install
%cmake_install

# Move config.fish from /usr/etc/fish/ to /etc/fish/ in the buildroot
if [ -f %{buildroot}/usr/etc/fish/config.fish ]; then
    mkdir -p %{buildroot}%{_sysconfdir}/fish
    mv %{buildroot}/usr/etc/fish/config.fish %{buildroot}%{_sysconfdir}/fish/config.fish
fi

%files
# Documentation (license.html is packaged separately as %%license below)
%exclude %{_docdir}/fish/license.html
%doc %{_docdir}/fish
%license LICENSE
# Executable files
%attr(0755,root,root) %{_bindir}/fish
%attr(0755,root,root) %{_bindir}/fish_indent
%attr(0755,root,root) %{_bindir}/fish_key_reader
# Config files and folders
%dir %{_sysconfdir}/fish/
%config(noreplace) %{_sysconfdir}/fish/config.fish
# fish.desktop and fish.png are not installed by %%install; left commented for reference
# %%{_datadir}/applications/fish.desktop
%exclude %{_datadir}/fish/man
%{_datadir}/fish/
%{_mandir}/man1/fish*.1*
# %%{_datadir}/pixmaps/fish.png
%{_datadir}/pkgconfig/fish.pc

%post
# Add fish to the list of allowed shells in /etc/shells
if ! grep %{_bindir}/fish %{_sysconfdir}/shells >/dev/null; then
    echo %{_bindir}/fish >>%{_sysconfdir}/shells
fi

%postun
# Remove fish from the list of allowed shells in /etc/shells
if [ "$1" = 0 ]; then
    sed -i "\|^%{_bindir}/fish\$|d" %{_sysconfdir}/shells
fi

%check
%{buildroot}%{_bindir}/fish --version

%changelog
%autochangelog
