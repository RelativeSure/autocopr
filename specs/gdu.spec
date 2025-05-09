%global debug_package %{nil}

Name:    gdu
Version: 5.24.0
Release: 1%{?dist}
Summary: Fast disk usage analyzer with console interface written in Go

License: MIT
URL:     https://github.com/dundee/gdu
Source0: https://github.com/dundee/gdu/archive/v%{version}.tar.gz

BuildRequires: golang >= 1.20
BuildRequires: git

%description
GDU (Go Disk Usage) is a fast disk usage analyzer with a console interface written in Go.

%prep
tar -xf %{SOURCE0}

%build
cd gdu-%{version}
export CGO_CPPFLAGS="${CPPFLAGS}"
export CGO_CFLAGS="${CFLAGS}"
export CGO_CXXFLAGS="${CXXFLAGS}"
export CGO_LDFLAGS="${LDFLAGS}"
go build -trimpath -buildmode=pie -mod=readonly -modcacherw -ldflags "-linkmode=external -X main.version=%{version}"

%install
rm -rf %{buildroot} && mkdir -p %{buildroot}%{_bindir}/ && cd gdu-%{version}
install -m 0755 gdu %{buildroot}%{_bindir}/gdu
mkdir -p %{buildroot}%{_datadir}/licenses/%{name}/
install -m 0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/

%files
%{_bindir}/gdu
%license %{_datadir}/licenses/%{name}/LICENSE
