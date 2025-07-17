%global debug_package %{nil}

Name:    lua-language-server
Version: 3.15.0
Release: 1%{?dist}
Summary: A language server that offers Lua language support - programmed in Lua

License: MIT
URL:     https://github.com/LuaLS/lua-language-server
BuildRequires: ninja-build
BuildRequires: git
BuildRequires: libstdc++-static

%description
%{summary}

%prep
git clone --recurse-submodules https://github.com/LuaLS/lua-language-server .

%build
%global _lto_cflags %{nil}
%global _lto_cxxflags %{nil}
./make.sh

%install
install -d -m 0755 %{buildroot}%{_libexecdir}/%{name}
cp -r bin/* %{buildroot}%{_libexecdir}/%{name}
install -d -m 0755 %{buildroot}%{_datadir}/%{name}
cp -r     debugger.lua     main.lua     locale     script     meta     %{buildroot}%{_datadir}/%{name}/
install -d -m 0755 %{buildroot}%{_bindir}
ln -s %{_libexecdir}/%{name}/lua-language-server %{buildroot}%{_bindir}/lua-language-server

%files
%doc README.md
%license LICENSE
%{_libexecdir}/%{name}
%{_datadir}/%{name}
%{_bindir}/lua-language-server

%changelog
%autochangelog
