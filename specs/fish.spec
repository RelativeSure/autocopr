%global debug_package %{nil}

Name:    fish
Version: 4.0.2
Release: 1%{?dist}
Summary: The user-friendly command line shell.

License: MIT
Requires:      ncurses-base
Requires:      file
Requires:      python3
Requires:      man
Requires:      procps-ng
URL:     https://github.com/fish-shell/fish-shell
Source:  %{url}/releases/download/%{version}/fish-static-amd64-%{version}.tar.xz
Source1: https://raw.githubusercontent.com/fish-shell/fish-shell/%{version}/README.rst
Source2: https://raw.githubusercontent.com/fish-shell/fish-shell/%{version}/COPYING

%description
Fish is a smart and user-friendly command line shell for Linux, macOS, and the rest
of the family. Fish includes features like syntax highlighting, autosuggestions,
and tab completions that just work, with nothing to learn or configure.

%prep
%autosetup -c
cp %{SOURCE1} README.md
cp %{SOURCE2} LICENSE

%install
install -v -p -D %{name} %{buildroot}%{_bindir}/%{name}
install -v -p -D %{name}_indent %{buildroot}%{_bindir}/%{name}_indent
install -v -p -D %{name}_key_reader %{buildroot}%{_bindir}/%{name}_key_reader

# Create a temporary directory for XDG_DATA_HOME
install -d -m0755 %{buildroot}/temp_xdg_data_home

# Run fish --install to extract data files
XDG_DATA_HOME=%{buildroot}/temp_xdg_data_home %{buildroot}%{_bindir}/fish --install

# Define the assumed base path where fish --install extracts files
# This is typically $XDG_DATA_HOME/fish/install/
EXTRACT_BASE_PATH="%{buildroot}/temp_xdg_data_home/fish/install"

# Create standard target directories
install -d -m0755 %{buildroot}%{_datadir}/fish
install -d -m0755 %{buildroot}%{_datadir}/pkgconfig
install -d -m0755 %{buildroot}%{_datadir}/applications
install -d -m0755 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps # Assuming SVG, adjust if PNG in pixmaps
install -d -m0755 %{buildroot}%{_mandir}/man1
install -d -m0755 %{buildroot}%{_docdir}/fish
install -d -m0755 %{buildroot}%{_sysconfdir}/fish/conf.d

# Move extracted files to their final destinations
# Fish data (completions, functions, etc.)
if [ -d "${EXTRACT_BASE_PATH}/share/fish" ]; then
  mv "${EXTRACT_BASE_PATH}/share/fish/"* %{buildroot}%{_datadir}/fish/
fi

# Man pages
if [ -d "${EXTRACT_BASE_PATH}/share/man/man1" ]; then
  mv "${EXTRACT_BASE_PATH}/share/man/man1/"* %{buildroot}%{_mandir}/man1/
fi

# Pkgconfig file
if [ -f "${EXTRACT_BASE_PATH}/share/pkgconfig/fish.pc" ]; then
  mv "${EXTRACT_BASE_PATH}/share/pkgconfig/fish.pc" %{buildroot}%{_datadir}/pkgconfig/
fi

# Desktop file
if [ -f "${EXTRACT_BASE_PATH}/share/applications/fish.desktop" ]; then
  mv "${EXTRACT_BASE_PATH}/share/applications/fish.desktop" %{buildroot}%{_datadir}/applications/
fi

# Icon file (assuming SVG)
if [ -f "${EXTRACT_BASE_PATH}/share/icons/hicolor/scalable/apps/fish.svg" ]; then
  mv "${EXTRACT_BASE_PATH}/share/icons/hicolor/scalable/apps/fish.svg" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
fi

# Install actual documentation (README.md and LICENSE from %prep)
install -v -p -m0644 README.md LICENSE %{buildroot}%{_docdir}/fish/

# Cleanup temporary directory
rm -rf %{buildroot}/temp_xdg_data_home

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}_indent
%{_bindir}/%{name}_key_reader
%doc %{_docdir}/fish
%{_mandir}/man1/*
%dir %{_sysconfdir}/fish
%dir %{_sysconfdir}/fish/conf.d
%{_datadir}/fish/
# The following line is for files that may be created by fish at runtime.
# These are not present at build time but should be owned by the package.
%ghost %{_datadir}/fish/generated_completions
%{_datadir}/pkgconfig/fish.pc
%{_datadir}/applications/fish.desktop
%{_datadir}/icons/hicolor/scalable/apps/fish.svg

%post
# Add fish to the list of allowed shells in /etc/shells
if ! grep %{_bindir}/fish %{_sysconfdir}/shells >/dev/null; then
    echo %{_bindir}/fish >>%{_sysconfdir}/shells
fi

%postun
# Remove fish from the list of allowed shells in /etc/shells
if [ "$1" = 0 ]; then # Check if it's a final removal (package uninstall)
    # Create a temporary file excluding the fish shell entry
    grep -v %{_bindir}/fish %{_sysconfdir}/shells > %{_sysconfdir}/shells.tmp
    # Replace the original /etc/shells with the temporary file
    mv %{_sysconfdir}/shells.tmp %{_sysconfdir}/shells
fi

%changelog
%autochangelog
