%global debug_package %{nil}

Name:    lua-language-server
Version: 3.13.2
Release: 1%{?dist}
Summary: A language server that offers Lua language support - programmed in Lua

License: MIT
# https://github.com/LuaLS/lua-language-server/releases/download/3.13.2/lua-language-server-3.13.2-linux-x64-musl.tar.gz
URL:     https://github.com/LuaLS/lua-language-server
Source:  %{url}/releases/download/%{version}/%{name}-%{version}-linux-x64-musl.tar.gz
Source1: https://raw.githubusercontent.com/LuaLS/lua-language-server/%{version}/README.md
Source2: https://raw.githubusercontent.com/LuaLS/lua-language-server/%{version}/LICENSE
ExcludeArch: s390x ppc64le ppc64

%description
%{summary}

%prep
%autosetup -c
cp %{SOURCE1} CONFIGURATION.md
cp %{SOURCE2} LICENSE

#%build

%install
install -d -m 0755 %{buildroot}%{_libexecdir}/%{name}
cp -av bin/* %{buildroot}%{_libexecdir}/%{name}
install -d -m 0755 %{buildroot}%{_datadir}/%{name}
cp -av \
    debugger.lua \
    main.lua \
    locale \
    script \
    meta \
    %{buildroot}%{_datadir}/%{name}/
install -d -m 0755 %{buildroot}%{_bindir}
#sed -e 's#@LIBEXECDIR@#%{_libexecdir}#' %{SOURCE1} > %{buildroot}%{_bindir}/%{name}
chmod 0755 %{buildroot}%{_bindir}/%{name}

%fdupes %{buildroot}%{_libexecdir}/%{name}
%fdupes %{buildroot}%{_datadir}/%{name}


%files
%doc CONFIGURATION.md
%license LICENSE
%{_bindir}/%{name}
%{_libexecdir}/%{name}/
%{_datadir}/%{name}/

%changelog
%autochangelog
