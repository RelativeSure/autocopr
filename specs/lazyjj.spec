%global debug_package %{nil}

Name:    lazyjj
Version: 0.5.0
Release: 1%{?dist}
Summary: TUI for Jujutsu/jj

License: Apache-2.0
# https://github.com/Cretezy/lazyjj/releases/download/v0.4.2/lazyjj-v0.4.2-x86_64-unknown-linux-musl.tar.gz
URL: https://github.com/Cretezy/lazyjj
Source: %{url}/releases/download/v%{version}/%{name}-v%{version}-x86_64-unknown-linux-musl.tar.gz
Source1: https://raw.githubusercontent.com/Cretezy/lazyjj/v%{version}/README.md
Source2: https://raw.githubusercontent.com/Cretezy/lazyjj/v%{version}/LICENSE

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
