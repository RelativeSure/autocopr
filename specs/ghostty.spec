%global debug_package %{nil}
%global tmp_dir /tmp/offline-cache
%global ghostty_tmp_dir /tmp/ghostty

Name:    ghostty
Version: 1.0.0
Release: 1%{?dist}
Summary: 👻 Ghostty is a fast, feature-rich, and cross-platform terminal emulator that uses platform-native UI and GPU acceleration.

# https://release.files.ghostty.org/VERSION/ghostty-source.tar.gz
# https://github.com/ghostty-org/ghostty/releases/download/tip/ghostty-source.tar.gz
# https://github.com/ghostty-org/ghostty/archive/refs/tags/v1.0.0.tar.gz
License: MIT
URL: https://github.com/ghostty-org/ghostty
Source:  %{url}/archive/refs/tags/v%{version}.tar.gz
Source1: https://raw.githubusercontent.com/ghostty-org/ghostty/v%{version}/README.md
Source2: https://raw.githubusercontent.com/ghostty-org/ghostty/v%{version}/LICENSE

# https://ghostty.org/docs/install/build#dependencies
BuildRequires: zig >= 0.13
BuildRequires: gtk4-devel
BuildRequires: libadwaita-devel
# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_desktop_files
BuildRequires: desktop-file-utils

%description
Ghostty is a terminal emulator that differentiates itself by being fast, feature-rich, and native.
While there are many excellent terminal emulators available, they all force you to choose between speed, features, or native UIs. 
Ghostty provides all three.
In all categories, I am not trying to claim that Ghostty is the best (i.e. the fastest, most feature-rich, or most native).
But when I set out to create Ghostty, I felt all terminals made you choose at most two of these categories.
I wanted to create a terminal that was competitive in all three categories and I believe Ghostty achieves that goal.
Before diving into the details, I also want to note that Ghostty is a passion project started by Mitchell Hashimoto

%prep
%autosetup -c
cp %{SOURCE1} CONFIGURATION.md
cp %{SOURCE2} LICENSE

%build
cd %{name}-%{version}
mkdir -p %{tmp_dir}
mkdir -p %{ghostty_tmp_dir}
#ZIG_GLOBAL_CACHE_DIR=%{tmp_dir} ./nix/build-support/fetch-zig-cache.sh
zig build -p %{ghostty_tmp_dir} -Doptimize=ReleaseFast
# Copy .desktop file
mkdir %{buildroot}%{_datadir}/applications/com.mitchellh.ghostty.desktop
cp %{ghostty_tmp_dir}/share/applications/com.mitchellh.ghostty.desktop %{buildroot}%{_datadir}/applications/com.mitchellh.ghostty.desktop

%install
install -pvD %{ghostty_tmp_dir}/bin/%{name} %{buildroot}%{_bindir}/%{name}
desktop-file-install --dir=%{buildroot}%{_datadir}/applications

# Shell completions
install -pvD -m 0644 %{ghostty_tmp_dir}/share/bash-completion/completions/%{name}.bash %{buildroot}%{bash_completions_dir}/%{name}
install -pvD -m 0644 %{ghostty_tmp_dir}/share/fish/vendor-completions.d/%{name}.fish %{buildroot}%{fish_completions_dir}/%{name}.fish
install -pvD -m 0644 %{ghostty_tmp_dir}/share/zsh/_%{name} %{buildroot}%{zsh_completions_dir}/_%{name}

%files
%doc CONFIGURATION.md
%license LICENSE
%{_bindir}/%{name}
%{buildroot}%{_datadir}/applications/com.mitchellh.ghostty
# Shell completions
%{buildroot}%{bash_completions_dir}/%{name}.bash
%{buildroot}%{fish_completions_dir}/%{name}.fish
%{buildroot}%{zsh_completions_dir}/_%{name}

%changelog
%autochangelog
