%global debug_package %{nil}
Name:    lua-language-server
Version: 3.16.1
Release: 1%{?dist}
Summary: A language server that offers Lua language support - programmed in Lua
License: MIT
URL:     https://github.com/LuaLS/lua-language-server
# Note: Using git instead of tarball because submodules are required for build
# Source0: %{url}/archive/refs/tags/%{version}.tar.gz

BuildRequires: fdupes
BuildRequires: gcc
BuildRequires: git
BuildRequires: gcc-c++
BuildRequires: libstdc++-static
BuildRequires: ninja-build

%description
%{summary}

%prep
# Clone specific version tag to ensure reproducible builds
git clone --recurse-submodules --depth 1 --branch %{version} %{url}

%build
cd lua-language-server
pushd 3rd/luamake
./compile/build.sh
popd
3rd/luamake/luamake rebuild

%install
cd lua-language-server
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libexecdir}/%{name}
mkdir -p %{buildroot}%{_datadir}/%{name}

# Install the main binary
install -m 755 bin/lua-language-server %{buildroot}%{_bindir}/%{name}

# Install support files
cp -r bin/* %{buildroot}%{_libexecdir}/%{name}/
cp -r meta %{buildroot}%{_datadir}/%{name}/
cp -r locale %{buildroot}%{_datadir}/%{name}/

%files
%doc lua-language-server/README.md
%license lua-language-server/LICENSE
%{_bindir}/%{name}
%{_libexecdir}/%{name}/
%{_datadir}/%{name}/

%changelog
%autochangelog
