%global debug_package %{nil}

Name:    nvm
Version: 0.40.3
Release: 2%{?dist}
Summary: Node Version Manager - POSIX-compliant bash script to manage multiple active node.js versions

License: MIT
URL:     https://github.com/nvm-sh/nvm
Source0: %{url}/archive/refs/tags/v%{version}.tar.gz
BuildArch: noarch

# Core tools nvm relies on at runtime
Requires: bash
Requires: coreutils
Requires: curl
Requires: tar
Requires: xz
Requires: findutils
Requires: grep
Requires: sed
Requires: ca-certificates
# For system-wide completion install (optional at runtime, but recommended)
Recommends: bash-completion

%description
%{summary}

%prep
%autosetup -p1

%build
# Nothing to build

%install
# Install nvm scripts to a system-wide location (/usr/share/nvm).
# nvm is per-user; we provide a loader that symlinks these into $NVM_DIR for each user.
install -d -m 755 %{buildroot}%{_datadir}/nvm
install -m 644 nvm.sh %{buildroot}%{_datadir}/nvm/
install -m 755 nvm-exec %{buildroot}%{_datadir}/nvm/

# Install bash completion to the standard completion directory
install -d -m 755 %{buildroot}%{_datadir}/bash-completion/completions
install -m 644 bash_completion %{buildroot}%{_datadir}/bash-completion/completions/nvm

# Bash/sh loader in /etc/profile.d
install -d -m 755 %{buildroot}%{_sysconfdir}/profile.d
cat > %{buildroot}%{_sysconfdir}/profile.d/nvm.sh << 'EOF'
# nvm system-wide loader (bash/sh)

# Default per-user NVM_DIR; users may override in their shell rc files
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"

# Ensure NVM_DIR exists and contains symlinks to system nvm files
if [ ! -e "$NVM_DIR/nvm.sh" ]; then
  mkdir -p "$NVM_DIR"
  ln -sf /usr/share/nvm/nvm.sh "$NVM_DIR/nvm.sh"
fi
if [ ! -e "$NVM_DIR/nvm-exec" ]; then
  ln -sf /usr/share/nvm/nvm-exec "$NVM_DIR/nvm-exec"
fi

# Load nvm if available
if [ -s "$NVM_DIR/nvm.sh" ]; then
  . "$NVM_DIR/nvm.sh"
fi
EOF
chmod 644 %{buildroot}%{_sysconfdir}/profile.d/nvm.sh

# Zsh loader (Fedora sources /etc/zshrc.d/*.zsh for interactive shells)
install -d -m 755 %{buildroot}%{_sysconfdir}/zshrc.d
cat > %{buildroot}%{_sysconfdir}/zshrc.d/nvm.zsh << 'EOF'
# nvm system-wide loader (zsh)

export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"

if [ ! -e "$NVM_DIR/nvm.sh" ]; then
  mkdir -p "$NVM_DIR"
  ln -sf /usr/share/nvm/nvm.sh "$NVM_DIR/nvm.sh"
fi
if [ ! -e "$NVM_DIR/nvm-exec" ]; then
  ln -sf /usr/share/nvm/nvm-exec "$NVM_DIR/nvm-exec"
fi

if [ -s "$NVM_DIR/nvm.sh" ]; then
  . "$NVM_DIR/nvm.sh"
fi
EOF
chmod 644 %{buildroot}%{_sysconfdir}/zshrc.d/nvm.zsh

%files
%doc README.md
%license LICENSE.md
%{_datadir}/nvm/
%{_datadir}/bash-completion/completions/nvm
%config(noreplace) %{_sysconfdir}/profile.d/nvm.sh
%config(noreplace) %{_sysconfdir}/zshrc.d/nvm.zsh

%changelog
%autochangelog
