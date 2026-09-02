%global debug_package %{nil}

Name:    zellij
Version: 0.45.1
Release: 1%{?dist}
Summary: A terminal workspace with batteries included

License:    MIT
URL:        https://github.com/zellij-org/zellij
Source:     %{url}/releases/download/v%{version}/%{name}-x86_64-unknown-linux-musl.tar.gz

%description
Zellij is a workspace aimed at developers, ops-oriented people and anyone
who loves the terminal. At its core, it is a terminal multiplexer (similar to
tmux and screen), but this is merely its infrastructure layer. Zellij includes
a layout system, and a plugin system allowing one to create plugins in any
language that compiles to WebAssembly.

%prep
# This source file doesn't have a high level directory, so create one
%autosetup -c

%build
# Generate shell completions
./%{name} setup --generate-completion bash > %{name}.bash
./%{name} setup --generate-completion zsh > _%{name}
./%{name} setup --generate-completion fish > %{name}.fish

%install
install -p -D %{name} %{buildroot}%{_bindir}/%{name}

# Shell completions
install -pvD -m 0644 %{name}.bash %{buildroot}%{bash_completions_dir}/%{name}
install -pvD -m 0644 _%{name} %{buildroot}%{zsh_completions_dir}/_%{name}
install -pvD -m 0644 %{name}.fish %{buildroot}%{fish_completions_dir}/%{name}.fish

%check
%{buildroot}%{_bindir}/%{name} --version

%files
%{_bindir}/%{name}
%{bash_completions_dir}/%{name}
%{zsh_completions_dir}/_%{name}
%{fish_completions_dir}/%{name}.fish

%changelog
%autochangelog
