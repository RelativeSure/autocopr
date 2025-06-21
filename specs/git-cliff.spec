%global debug_package %{nil}

Name:    git-cliff
Version: 2.8.0
Release: 1%{?dist}
Summary: A highly customizable Changelog Generator that follows Conventional Commit specifications ⛰️

License: Apache v2.0
URL: https://github.com/orhun/git-cliff
Source0: %{url}/releases/download/v%{version}/%{name}-v%{version}-x86_64-unknown-linux-musl.tar.gz
Source1: https://raw.githubusercontent.com/orhun/git-cliff/v%{version}/README.md
Source2: https://raw.githubusercontent.com/orhun/git-cliff/v%{version}/LICENSE-APACHE

%description
%{summary}

%prep
%autosetup -c -n %{name}-v%{version}-x86_64-unknown-linux-musl
cp %{SOURCE1} CONFIGURATION.md
cp %{SOURCE2} LICENSE

%build

%install
install -p -D %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 0644 CONFIGURATION.md %{buildroot}%{_docdir}/%{name}/README.md
install -D -m 0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%files
%doc %{_docdir}/%{name}/README.md
%license %{_datadir}/licenses/%{name}/LICENSE
%{_bindir}/%{name}

%changelog
%autochangelog
