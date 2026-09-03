%global debug_package %{nil}

Name:    git-cliff
Version: 2.14.1
Release: 1%{?dist}
Summary: A highly customizable changelog generator that follows Conventional Commits

License:    MIT OR Apache-2.0
URL:        https://github.com/orhun/git-cliff
Source:     %{url}/releases/download/v%{version}/%{name}-%{version}-x86_64-unknown-linux-musl.tar.gz

%description
%{summary}.

%prep
%autosetup -n %{name}-%{version}

%build

%install
install -p -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -p -D -m 0644 man/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -pvD -m 0644 completions/%{name}.bash %{buildroot}%{bash_completions_dir}/%{name}
install -pvD -m 0644 completions/_%{name} %{buildroot}%{zsh_completions_dir}/_%{name}
install -pvD -m 0644 completions/%{name}.fish %{buildroot}%{fish_completions_dir}/%{name}.fish

%check
%{buildroot}%{_bindir}/%{name} --version

%files
%doc README.md
%doc CHANGELOG.md
%license LICENSE-MIT
%license LICENSE-APACHE
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{bash_completions_dir}/%{name}
%{zsh_completions_dir}/_%{name}
%{fish_completions_dir}/%{name}.fish

%changelog
%autochangelog
