###
# Inspiration taken from https://gitlab.com/pgill/ghostty-rpm
###
%global debug_package %{nil}

Name:           ghostty
Version:        1.2.0
Release:        1%{?dist}
Summary:        Fast, feature-rich, and cross-platform terminal emulator that uses platform-native UI and GPU acceleration

License:        MIT
URL:            https://github.com/ghostty-org/ghostty
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

ExclusiveArch:  x86_64

BuildRequires:  appstream
BuildRequires:  blueprint-compiler >= 0.16.0
BuildRequires:  desktop-file-utils
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk4-devel
BuildRequires:  gtk4-layer-shell-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  libadwaita-devel
BuildRequires:  libpng-devel
BuildRequires:  oniguruma-devel
BuildRequires:  pandoc-cli
BuildRequires:  pixman-devel
BuildRequires:  pkg-config
BuildRequires:  systemd-rpm-macros
BuildRequires:  wayland-protocols-devel
BuildRequires:  zig >= 0.14.0
BuildRequires:  zlib-ng-devel

Requires:       fontconfig
Requires:       freetype
Requires:       glib2
Requires:       gtk4
Requires:       gtk4-layer-shell
Requires:       harfbuzz
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       libpng
Requires:       oniguruma
Requires:       pixman
Requires:       zlib-ng
Requires(post): desktop-file-utils
Requires(post): gtk-update-icon-cache
Requires(postun): desktop-file-utils
Requires(postun): gtk-update-icon-cache

%description
%{summary}

%prep
%setup -q -n ghostty-%{version}

%build
export ZIG_GLOBAL_CACHE_DIR="%{_builddir}/.zig-cache"
export HOME="%{_builddir}"
export DESTDIR="%{_builddir}/.destdir"
zig build \
    --summary all \
    -Dversion-string=%{version}-%{release} \
    -Doptimize=ReleaseFast \
    -Dcpu=baseline \
    -Dpie=true \
    -Demit-docs \
    --prefix "%{_prefix}"

%install
rm -rf %{buildroot}
export ZIG_GLOBAL_CACHE_DIR="%{_builddir}/.zig-cache"
export HOME="%{_builddir}"
export DESTDIR="%{buildroot}"
zig build install \
    --summary all \
    -Dversion-string=%{version}-%{release} \
    -Doptimize=ReleaseFast \
    -Dcpu=baseline \
    -Dpie=true \
    -Demit-docs \
    --prefix "%{_prefix}" \
    --system "%{_builddir}/.zig-cache/p"

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/com.mitchellh.ghostty.desktop
appstreamcli validate --no-net %{buildroot}%{_datadir}/metainfo/com.mitchellh.ghostty.metainfo.xml

%post
update-desktop-database -q %{_datadir}/applications || :
gtk-update-icon-cache -q %{_datadir}/icons/hicolor || :

%postun
update-desktop-database -q %{_datadir}/applications || :
gtk-update-icon-cache -q %{_datadir}/icons/hicolor || :


%files
%license LICENSE
%{_bindir}/ghostty
%{_datadir}/applications/com.mitchellh.ghostty.desktop
%{_datadir}/bash-completion/completions/ghostty.bash
%{_datadir}/bat/syntaxes/ghostty.sublime-syntax
%{_datadir}/dbus-1/services/com.mitchellh.ghostty.service
%{_datadir}/fish/vendor_completions.d/ghostty.fish
%{_datadir}/ghostty
%{_datadir}/icons/hicolor/*/apps/com.mitchellh.ghostty.png
%{_datadir}/kio/servicemenus/com.mitchellh.ghostty.desktop
%{_datadir}/man/man1/ghostty.1*
%{_datadir}/man/man5/ghostty.5*
%{_datadir}/metainfo/com.mitchellh.ghostty.metainfo.xml
%{_datadir}/nautilus-python/extensions/ghostty.py
%{_datadir}/nvim/site/compiler/ghostty.vim
%{_datadir}/nvim/site/ftdetect/ghostty.vim
%{_datadir}/nvim/site/ftplugin/ghostty.vim
%{_datadir}/nvim/site/syntax/ghostty.vim
%{_datadir}/locale/*/LC_MESSAGES/com.mitchellh.ghostty.mo
%{_datadir}/terminfo/g/ghostty
%{_datadir}/terminfo/x/xterm-ghostty
%{_datadir}/vim/vimfiles/compiler/ghostty.vim
%{_datadir}/vim/vimfiles/ftdetect/ghostty.vim
%{_datadir}/vim/vimfiles/ftplugin/ghostty.vim
%{_datadir}/vim/vimfiles/syntax/ghostty.vim
%{_datadir}/zsh/site-functions/_ghostty
%{_userunitdir}/app-com.mitchellh.ghostty.service


%changelog
%autochangelog
