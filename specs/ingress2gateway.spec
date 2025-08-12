%global debug_package %{nil}

Name:    ingress2gateway
Version: 0.4.0
Release: 1%{?dist}
Summary: A tool to convert Ingress resources to Gateway API resources

License: Apache-2.0
URL:     https://github.com/kubernetes-sigs/ingress2gateway
Source0: https://github.com/kubernetes-sigs/ingress2gateway/archive/v%{version}.tar.gz

BuildRequires: golang >= 1.22
BuildRequires: git

%description
A tool to convert Ingress resources to Gateway API resources.

%prep
%autosetup -n ingress2gateway-%{version}

%build
export CGO_CPPFLAGS="${CPPFLAGS}"
export CGO_CFLAGS="${CFLAGS}"
export CGO_CXXFLAGS="${CXXFLAGS}"
export CGO_LDFLAGS="${LDFLAGS}"
go build \
    -trimpath \
    -buildmode=pie \
    -mod=readonly \
    -modcacherw \
    -ldflags "-linkmode=external -X main.version=%{version}" \
    ./cmd/ingress2gateway

%install
rm -rf %{buildroot}
install -D -m 0755 ingress2gateway %{buildroot}%{_bindir}/ingress2gateway
install -D -m 0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%verifyscript
%{buildroot}%{_bindir}/ingress2gateway --help

%files
%{_bindir}/ingress2gateway
%license %{_datadir}/licenses/%{name}/LICENSE

%changelog
%autochangelog
