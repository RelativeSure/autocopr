%global debug_package %{nil}

Name: dua-cli
Version: 2.31.0
Release: 1%{?dist}
Summary: A fast tool for disk usage analysis

License: MIT
URL: https://github.com/Byron/dua-cli
Source0: %{url}/releases/download/v%{version}/dua-v%{version}-x86_64-unknown-linux-musl.tar.gz
Source1: %{url}/releases/download/v%{version}/completions.tar.gz
Source2: https://raw.githubusercontent.com/Byron/dua-cli/v%{version}/LICENSE

BuildRequires: gzip

%description
%{summary}

%prep
%autosetup -c -n dua-v%{version}-x86_64-unknown-linux-musl
# autosetup can't extract more than one tarball, extract manually
# https://github.com/rpm-software-management/rpm/issues/2495
%__rpmuncompress -x %{SOURCE1}
cp %{SOURCE2} .

%build

%install
install -p -D dua %{buildroot}%{_bindir}/dua

# Shell completion
install -v -p -D -m 0644 completions/dua.bash %{buildroot}%{_datadir}/bash-completion/completions/dua
install -v -p -D -m 0644 completions/dua.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/dua.fish
install -v -p -D -m 0644 completions/_dua %{buildroot}%{_datadir}/zsh/site-functions/_dua

%files
%{_bindir}/dua
%{bash_completions_dir}/dua
%{zsh_completions_dir}/_dua
%{fish_completions_dir}/dua.fish
%license LICENSE

%changelog
%autochangelog
