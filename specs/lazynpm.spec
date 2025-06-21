%global debug_package %{nil}

Name:    lazynpm
Version: 0.1.4
Release: 1%{?dist}
Summary: terminal UI for npm

License: MIT
URL: https://github.com/jesseduffield/lazynpm
Source: %{url}/releases/download/v%{version}/%{name}_%{version}_Linux_x86_64.tar.gz
Source1: https://raw.githubusercontent.com/jesseduffield/lazynpm/v%{version}/README.md
Source2: https://raw.githubusercontent.com/jesseduffield/lazynpm/v%{version}/LICENSE

%description
%{summary}

%prep
%autosetup -c
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
