%global debug_package %{nil}
%global raw_ghuc https://raw.githubusercontent.com/bvaisvil/zenith/

Name:    zenith
Version: 0.15.0
Release: 1%{?dist}
Summary: Terminal system monitor with zoom-able charts for CPU, GPU, network, and disk

License: MIT
# https://github.com/bvaisvil/zenith/releases/download/0.15.0/zenith-Linux-musl-x86_64.tar.gz
URL:     https://github.com/bvaisvil/zenith
Source:  %{url}/releases/download/%{version}/%{name}-Linux-musl-x86_64.tar.gz
Source1: %{raw_ghuc}/%{version}/README.md
Source2: %{raw_ghuc}/%{version}/LICENSE

%description
%{summary}

%prep
%autosetup -c
cp %{SOURCE1} CONFIGURATION.md
cp %{SOURCE2} LICENSE

%build

%install
install -p -D %{name} %{buildroot}%{_bindir}/%{name}

%files
%doc CONFIGURATION.md
%license LICENSE
%{_bindir}/%{name}

%check
%{buildroot}%{_bindir}/%{name} --version

%changelog
%autochangelog
