%global debug_package %{nil}

Name:    ingress2gateway
Version: 1.2.0
Release: 1%{?dist}
Summary: Convert Ingress resources to Gateway API resources

License: Apache-2.0
URL:     https://github.com/kubernetes-sigs/ingress2gateway
Source0: %{url}/archive/v%{version}.tar.gz

BuildRequires: golang >= 1.25
BuildRequires: git

%description
%{summary}.

%prep
%autosetup -n %{name}-%{version}

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
    -ldflags "-linkmode=external -X github.com/kubernetes-sigs/ingress2gateway/pkg/i2gw.Version=%{version}" \
    -o %{name} .

%install
install -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%check
%{buildroot}%{_bindir}/%{name} version

%files
%{_bindir}/%{name}
%license %{_datadir}/licenses/%{name}/LICENSE

%changelog
%autochangelog
