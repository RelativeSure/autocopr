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


%description
bandwhich sniffs a given network interface and records IP packet size,
cross referencing it with the /proc filesystem on linux. It is responsive
to the terminal window size, displaying less info if there is no room for
it. It will also attempt to resolve ips to their host name in the
background using reverse DNS on a best effort basis.

%prep
%autosetup -c
cp %{SOURCE1} README.md
cp %{SOURCE2} CHANGELOG.md
cp %{SOURCE3} LICENSE.md

%build
./%{name} --generate-completions bash > %{name}.bash
./%{name} --generate-completions zsh > _%{name}
./%{name} --generate-completions fish > %{name}.fish

%install
install -p -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -pvD -m 0644 %{name}.bash %{buildroot}%{bash_completions_dir}/%{name}
install -pvD -m 0644 _%{name} %{buildroot}%{zsh_completions_dir}/_%{name}
install -pvD -m 0644 %{name}.fish %{buildroot}%{fish_completions_dir}/%{name}.fish

%files
%doc README.md
%doc CHANGELOG.md
%license LICENSE.md
%{_bindir}/%{name}
%{bash_completions_dir}/%{name}
%{zsh_completions_dir}/_%{name}
%{fish_completions_dir}/%{name}.fish

%check
%{buildroot}%{_bindir}/%{name} --version

%changelog
%autochangelog
