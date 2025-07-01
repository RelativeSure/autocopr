%global debug_package %{nil}

Name: zig
Version: 0.13.0
Release: 1%{?dist}
Summary: A general-purpose programming language and toolchain for maintaining robust, optimal, and reusable software.

License: MIT
URL: https://ziglang.org
Source0: https://ziglang.org/download/%{version}/zig-linux-x86_64-%{version}.tar.xz

%description
%{summary}

%prep
# -n specifies the directory name inside the tarball
%autosetup -n zig-linux-x86_64-%{version}

%build
# Nothing to build, using pre-compiled binaries

%install
# Install the main executable
install -p -D zig %{buildroot}%{_bindir}/zig

# Install the standard library files
# These are expected by the zig compiler to be in a relative path (e.g., ../lib)
# or a system-wide path. For a system package, a shared location is better.
# We'll place them in %{_datadir}/zig/lib
install -p -D -m 0644 README.md %{buildroot}%{_datadir}/%{name}/README.md
install -d %{buildroot}%{_datadir}/%{name}/lib
# Recursively copy the lib directory
cp -pr lib/* %{buildroot}%{_datadir}/%{name}/lib/

# Copy the license file
install -p -D -m 0644 LICENSE %{buildroot}%{_datadir}/%{name}/LICENSE

%files
%{_bindir}/zig
%doc %{_datadir}/%{name}/README.md
%license %{_datadir}/%{name}/LICENSE
%{_datadir}/%{name}/lib

%changelog
%autochangelog
