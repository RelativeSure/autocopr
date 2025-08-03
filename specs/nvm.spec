%global debug_package %{nil}

Name:    nvm
Version: 0.40.3
Release: 1%{?dist}
Summary: Node Version Manager - POSIX-compliant bash script to manage multiple active node.js versions

License: MIT
URL:     https://github.com/nvm-sh/nvm
Source0: %{url}/archive/refs/tags/v%{version}.tar.gz

%description
%{summary}

%prep
%autosetup -p1

%build
# Nothing to build

%install
# nvm is designed to be installed per-user. This spec file installs the nvm
# scripts to a system-wide location, and then provides a profile script that
# copies the necessary files to the user's home directory on first use. This
# approach respects the per-user design of nvm while allowing it to be
# managed by the system's package manager.

# Install nvm scripts to a system-wide location (/usr/share/nvm)
# This directory will serve as a template for the user's nvm installation.
install -d -m 755 %{buildroot}%{_datadir}/nvm
install -m 755 nvm.sh %{buildroot}%{_datadir}/nvm/
install -m 755 nvm-exec %{buildroot}%{_datadir}/nvm/
install -m 644 bash_completion %{buildroot}%{_datadir}/nvm/

# Install the profile script to /etc/profile.d/
# This script will be sourced by all users on login.
install -d -m 755 %{buildroot}%{_sysconfdir}/profile.d
cat << 'EOF' > %{buildroot}%{_sysconfdir}/profile.d/nvm.sh
# Setup nvm environment for the user.

# Set NVM_DIR to the default location if it's not already set.
# Users can override this by setting NVM_DIR in their own profile.
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"

# If the nvm scripts are not present in the user's NVM_DIR,
# copy them from the system-wide location. This is done only once.
if [ ! -s "$NVM_DIR/nvm.sh" ]; then
  mkdir -p "$NVM_DIR"
  cp /usr/share/nvm/nvm.sh "$NVM_DIR/nvm.sh"
  cp /usr/share/nvm/nvm-exec "$NVM_DIR/nvm-exec"
  cp /usr/share/nvm/bash_completion "$NVM_DIR/bash_completion"
fi

# Source nvm.sh to make the 'nvm' command available.
if [ -s "$NVM_DIR/nvm.sh" ]; then
  # This loads nvm
  . "$NVM_DIR/nvm.sh"
  # This loads nvm bash_completion
  # The bash completion script is compatible with zsh as well.
  [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
fi
EOF
chmod 644 %{buildroot}%{_sysconfdir}/profile.d/nvm.sh

%files
%doc README.md
%license LICENSE.md
%{_datadir}/nvm/
%{_sysconfdir}/profile.d/nvm.sh

%changelog
%autochangelog
