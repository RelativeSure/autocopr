%global debug_package %{nil}

Name:    feh
Version: 3.10.3
Release: 1%{?dist}
Summary: a fast and light image viewer

License: MIT-feh
URL:     https://github.com/derf/feh
Source0: https://feh.finalrewind.org/feh-%{version}.tar.bz2

BuildRequires: make
BuildRequires: imlib2-devel
BuildRequires: libcurl-devel
BuildRequires: libpng-devel
BuildRequires: libX11-devel
BuildRequires: libXt-devel
BuildRequires: libXinerama-devel
BuildRequires: libexif-devel
BuildRequires: file-devel

%description
%{summary}

%prep
%setup -q

%build
%make_build

%install
%make_install

%files
%{_bindir}/feh
%{_datadir}/applications/feh.desktop
%{_datadir}/feh/
%{_mandir}/man1/feh.1*
%{_datadir}/icons/hicolor/48x48/apps/feh.png

%changelog
%autochangelog
