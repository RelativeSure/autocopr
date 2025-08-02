%global debug_package %{nil}

Name:    has
Version: 1.5.2
Release: 1%{?dist}
Summary: checks presence of various command line tools and their versions on the path

License: MIT
URL:     https://github.com/kdabir/has
Source0: https://github.com/kdabir/has/archive/v%{version}.tar.gz

BuildRequires: bash
BuildRequires: git
BuildRequires: make

%description
has checks presence of various command line tools on the PATH and reports their installed version.

%prep
%autosetup -n has-%{version}

%build
# Nothing to build

%install
rm -rf %{buildroot}
make install PREFIX=%{buildroot}%{_prefix}

%files
%license LICENSE
%{_bindir}/has
