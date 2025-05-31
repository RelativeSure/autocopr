%global debug_package %{nil}

Name:    kubeswitch
Version: 0.9.3
Release: 1%{?dist}
Summary: The kubectx for operators.

License: Apache-2.0
URL:     https://github.com/danielfoehrKn/kubeswitch
Source0: %{URL}/releases/download/%{version}/switcher_linux_amd64
Source1: https://raw.githubusercontent.com/danielfoehrKn/kubeswitch/%{version}/README.md
Source2: https://raw.githubusercontent.com/danielfoehrKn/kubeswitch/%{version}/LICENSE

%description
%{summary}

%prep
cp %{SOURCE1} .
cp %{SOURCE2} .

%install
install -D -m 0755 %{SOURCE0} %{buildroot}%{_bindir}/kubeswitch
install -D -m 0644 README.md %{buildroot}%{_docdir}/%{name}/README.md
install -D -m 0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%files
%{_bindir}/kubeswitch
%license %{_datadir}/licenses/%{name}/LICENSE
%doc %{_docdir}/%{name}/README.md

%changelog
%autochangelog
