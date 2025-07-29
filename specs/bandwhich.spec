%global debug_package %{nil}

Name:    bandwhich
Version: 0.23.1
Release: 1%{?dist}
Summary: Terminal bandwidth utilization tool

License:    MIT
URL:        https://github.com/imsnif/bandwhich
Source:     %{url}/releases/download/v%{version}/%{name}-v%{version}-x86_64-unknown-linux-musl.tar.gz
Source1:    https://raw.githubusercontent.com/imsnif/bandwhich/v%{version}/README.md
Source2:    https://raw.githubusercontent.com/imsnif/bandwhich/v%{version}/CHANGELOG.md
Source3:    https://raw.githubusercontent.com/imsnif/bandwhich/v%{version}/LICENSE.md

BuildRequires: glibc
BuildRequires: gcc
BuildRequires: python3-kobo-rpmlib

%description
%{summary}

%prep
%autosetup -c
cp %{SOURCE1} README.md
cp %{SOURCE2} CHANGELOG.md
cp %{SOURCE3} LICENSE.md

%build

%install
install -p -D %{name} %{buildroot}%{_bindir}/%{name}

%files
%doc README.md
%doc CHANGELOG.md
%license LICENSE.md
%{_bindir}/%{name}
