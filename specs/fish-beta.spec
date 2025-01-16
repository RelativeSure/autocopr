%global debug_package %{nil}
%global binary_name fish

Name:    fish-beta
Version: 4.0b1
Release: 1%{?dist}
Summary: The user-friendly command line shell.

License: MIT
Source:  https://github.com/fish-shell/fish-shell/releases/download/%{version}/fish-static-linux-x86_64.tar.xz

%description
%{summary}

%prep
%autosetup -c

%install
install -v -p -D %{binary_name} %{buildroot}%{_bindir}/%{binary_name}
install -v -p -D %{binary_name}_indent %{buildroot}%{_bindir}/%{binary_name}_indent
install -v -p -D %{binary_name}_key_reader %{buildroot}%{_bindir}/%{binary_name}_key_reader

%autochangelog
