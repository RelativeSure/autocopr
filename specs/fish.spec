%global debug_package %{nil}

Name:    fish
Version: 4.0.2
Release: 1%{?dist}
Summary: The user-friendly command line shell.

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

%description
Fish is a smart and user-friendly command line shell for Linux, macOS, and the rest
of the family. Fish includes features like syntax highlighting, autosuggestions,
and tab completions that just work, with nothing to learn or configure.


%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1} README.md
cp %{SOURCE2} LICENSE

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%doc README.md
%license LICENSE
# Executable files
%{_bindir}/fish
%{_bindir}/fish_indent
%{_bindir}/fish_key_reader
# Config files and folders
-%config(noreplace) /usr/etc/fish/config.fish
+%config(noreplace) %{_sysconfdir}/fish/config.fish
%{_datadir}/applications/fish.desktop
%{_docdir}/fish/
%{_datadir}/fish/
%{_mandir}/man1/fish*.1*
%{_datadir}/pixmaps/fish.png
%{_libdir}/pkgconfig/fish.pc

%changelog
%autochangelog
