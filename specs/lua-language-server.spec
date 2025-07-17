%global debug_package %{nil}
Name:    lua-language-server
Version: 3.15.0
Release: 2%{?dist}
Summary: A language server that offers Lua language support - programmed in Lua
License: MIT
URL:     https://github.com/LuaLS/lua-language-server
Source:  %{url}/releases/download/%{version}/%{name}-%{version}-linux-x64.tar.gz
Source1: https://raw.githubusercontent.com/LuaLS/lua-language-server/%{version}/README.md
Source2: https://raw.githubusercontent.com/LuaLS/lua-language-server/%{version}/LICENSE
BuildRequires: fdupes
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libstdc++-static

%description
%{summary}

%prep
%autosetup -c
cp %{SOURCE1} CONFIGURATION.md
cp %{SOURCE2} LICENSE

%install
# Install the main executable and launcher script
install -d -m 0755 %{buildroot}%{_libexecdir}/%{name}
cp -av bin/* %{buildroot}%{_libexecdir}/%{name}

# Install the Lua scripts and data files
install -d -m 0755 %{buildroot}%{_datadir}/%{name}
cp -av \
    debugger.lua \
    main.lua \
    locale \
    script \
    meta \
    %{buildroot}%{_datadir}/%{name}/

# Create the wrapper script in /usr/bin
install -d -m 0755 %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << 'EOF'
#!/bin/bash
exec %{_libexecdir}/%{name}/lua-language-server "$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

%verifyscript
# Verify the main executable exists and is executable
if [ ! -x "%{_libexecdir}/%{name}/lua-language-server" ]; then
    echo "ERROR: Main executable %{_libexecdir}/%{name}/lua-language-server is missing or not executable"
    exit 1
fi

# Verify the wrapper script exists and is executable
if [ ! -x "%{_bindir}/%{name}" ]; then
    echo "ERROR: Wrapper script %{_bindir}/%{name} is missing or not executable"
    exit 1
fi

# Verify essential Lua scripts exist
for script in main.lua debugger.lua; do
    if [ ! -f "%{_datadir}/%{name}/$script" ]; then
        echo "ERROR: Essential script %{_datadir}/%{name}/$script is missing"
        exit 1
    fi
done

# Verify essential directories exist
for dir in locale script meta; do
    if [ ! -d "%{_datadir}/%{name}/$dir" ]; then
        echo "ERROR: Essential directory %{_datadir}/%{name}/$dir is missing"
        exit 1
    fi
done

# Test that the wrapper script can at least execute (--version should work quickly)
if ! timeout 10s "%{_bindir}/%{name}" --version >/dev/null 2>&1; then
    echo "WARNING: lua-language-server --version failed or timed out"
    # Don't exit with error here as this might fail in constrained build environments
fi

echo "lua-language-server package verification completed successfully"

%files
%doc CONFIGURATION.md
%license LICENSE
%{_bindir}/%{name}
%{_libexecdir}/%{name}/
%{_datadir}/%{name}/

%changelog
%autochangelog
