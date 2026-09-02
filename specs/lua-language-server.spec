%global debug_package %{nil}
Name:    lua-language-server
Version: 3.19.1
Release: 1%{?dist}
Summary: A language server that offers Lua language support - programmed in Lua
License: MIT
URL:     https://github.com/LuaLS/lua-language-server
# Note: Using git instead of tarball because submodules are required for build
# Source0: %%{url}/archive/refs/tags/%%{version}.tar.gz

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

# Install support files, then symlink the bindir entry to the libexec
# copy instead of installing the binary twice (avoids hardlinking across
# what may be separate partitions for /usr/bin and /usr/libexec)
cp -r bin/* %{buildroot}%{_libexecdir}/%{name}/
ln -s %{_libexecdir}/%{name}/lua-language-server %{buildroot}%{_bindir}/%{name}
cp -r meta %{buildroot}%{_datadir}/%{name}/
cp -r locale %{buildroot}%{_datadir}/%{name}/

# Drop .git gitlink files left over from the submodule checkouts; they're
# not real repos and have no business being shipped in the package
find %{buildroot}%{_datadir}/%{name}/meta -name '.git' -delete

%check
# The binary has no --version/--help flag; run with no arguments, it
# starts an LSP server loop that blocks reading stdin, so it can't be
# smoke-tested by invoking it directly without risking a hung build.
# Instead verify the compiled binary and its runtime-required main.lua
# are both present and executable in the expected layout.
test -x %{buildroot}%{_libexecdir}/%{name}/lua-language-server
test -f %{buildroot}%{_libexecdir}/%{name}/main.lua

%files
%doc lua-language-server/README.md
%license lua-language-server/LICENSE
%{_bindir}/%{name}
%{_libexecdir}/%{name}/
%{_datadir}/%{name}/

%changelog
%autochangelog
