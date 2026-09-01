###
# Inspiration taken from https://github.com/scottames/copr/blob/main/ghostty/ghostty.spec
###
%global debug_package %{nil}

# Ghostty 1.3.1 requires Zig 0.15.2 exactly (build.zig hard-errors on any other
# version) and Fedora's zig package has already moved past it (Zig lacks a
# stable API across minor versions, and Fedora doesn't keep old ones around).
# Zig 0.16 support only exists on ghostty's unreleased main branch. So the
# matching Zig toolchain is vendored here as a build-only tool rather than
# taken from the distro, the same way Source0 is already fetched over the
# network during the (network-enabled) buildsrpm stage and then used offline
# in the isolated mock chroot.
%global zigver 0.15.2
%global zig_sha256_x86_64 02aa270f183da276e5b5920b1dac44a63f1a49e55050ebde3aecc9eb82f93239
%global zig_sha256_aarch64 958ed7d1e00d0ea76590d27666efbf7a932281b3d7ba0c6b01b0ff26498f667f

Name:           ghostty
Version:        1.3.1
Release:        7%{?dist}
Summary:        Fast, feature-rich, and cross-platform terminal emulator that uses platform-native UI and GPU acceleration

License:        MIT
URL:            https://github.com/ghostty-org/ghostty
Source0:        https://github.com/ghostty-org/ghostty/archive/refs/tags/v%{version}.tar.gz
Source1:        https://ziglang.org/download/%{zigver}/zig-x86_64-linux-%{zigver}.tar.xz
Source2:        https://ziglang.org/download/%{zigver}/zig-aarch64-linux-%{zigver}.tar.xz

ExclusiveArch: x86_64 aarch64

BuildRequires: blueprint-compiler
BuildRequires: bzip2-devel
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: glib2-devel
BuildRequires: gtk4-devel
BuildRequires: gtk4-layer-shell-devel
BuildRequires: harfbuzz-devel
BuildRequires: libadwaita-devel
BuildRequires: libpng-devel
BuildRequires: oniguruma-devel
BuildRequires: pandoc-cli
BuildRequires: pixman-devel
BuildRequires: pkg-config
BuildRequires: wayland-protocols-devel
BuildRequires: xz
BuildRequires: zlib-ng-devel

Requires: fontconfig
Requires: freetype
Requires: glib2
Requires: gtk4
Requires: harfbuzz
Requires: libadwaita
Requires: libpng
Requires: oniguruma
Requires: pixman
Requires: zlib-ng

%description
%{summary}.

%package        devel
Summary:        Development files for libghostty-vt
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package provides the development files for libghostty-vt.

%prep
%setup -q -n ghostty-%{version}

%ifarch x86_64
echo "%{zig_sha256_x86_64}  %{SOURCE1}" | sha256sum -c -
%endif
%ifarch aarch64
echo "%{zig_sha256_aarch64}  %{SOURCE2}" | sha256sum -c -
%endif
mkdir -p ../zig-toolchain
%ifarch x86_64
tar -xf %{SOURCE1} -C ../zig-toolchain --strip-components=1
%endif
%ifarch aarch64
tar -xf %{SOURCE2} -C ../zig-toolchain --strip-components=1
%endif

%build
export PATH="%{_builddir}/zig-toolchain:$PATH"

# Link the system fontconfig/freetype/harfbuzz rather than letting zig vendor
# them. Without -fsys=, zig statically links its own copies *and* exports their
# symbols from the executable, while GTK4 separately pulls in the system libs.
# The executable wins global symbol resolution, so GTK's Fc*/FT_*/hb_* calls are
# interposed into the vendored copies while operating on system-lib state.
DESTDIR=%{buildroot} zig build \
    --summary all \
    --prefix "%{_prefix}" \
    -fsys=fontconfig \
    -fsys=freetype \
    -fsys=harfbuzz \
    -Dversion-string=%{version}-%{release} \
    -Doptimize=ReleaseFast \
    -Dcpu=baseline \
    -Dpie=true \
    -Dstrip=false \
    -Demit-docs \
    -Demit-themes=true

%if 0%{?fedora} >= 42
    rm -f "%{buildroot}%{_prefix}/share/terminfo/g/ghostty"
%endif

%files
%license LICENSE
%{_bindir}/ghostty
%{_prefix}/share/applications/com.mitchellh.ghostty.desktop
%{_prefix}/share/bash-completion/completions/ghostty.bash
%{_prefix}/share/bat/syntaxes/ghostty.sublime-syntax
%{_prefix}/share/fish/vendor_completions.d/ghostty.fish
%{_prefix}/share/ghostty
%{_prefix}/share/icons/hicolor/1024x1024/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/128x128/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/128x128@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/16x16/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/16x16@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/256x256/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/256x256@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/32x32/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/32x32@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/512x512/apps/com.mitchellh.ghostty.png
%{_prefix}/share/kio/servicemenus/com.mitchellh.ghostty.desktop
%{_prefix}/share/man/man1/ghostty.1
%{_prefix}/share/man/man5/ghostty.5
%{_prefix}/share/nautilus-python/extensions/ghostty.py
%{_prefix}/share/nvim/site/compiler/ghostty.vim
%{_prefix}/share/nvim/site/ftdetect/ghostty.vim
%{_prefix}/share/nvim/site/ftplugin/ghostty.vim
%{_prefix}/share/nvim/site/syntax/ghostty.vim
%{_prefix}/share/vim/vimfiles/compiler/ghostty.vim
%{_prefix}/share/vim/vimfiles/ftdetect/ghostty.vim
%{_prefix}/share/vim/vimfiles/ftplugin/ghostty.vim
%{_prefix}/share/vim/vimfiles/syntax/ghostty.vim
%{_prefix}/share/zsh/site-functions/_ghostty
%{_prefix}/share/dbus-1/services/com.mitchellh.ghostty.service
%{_prefix}/share/locale/*/LC_MESSAGES/com.mitchellh.ghostty.mo
%{_prefix}/share/metainfo/com.mitchellh.ghostty.metainfo.xml
%{_prefix}/share/systemd/user/app-com.mitchellh.ghostty.service
%{_prefix}/lib/libghostty-vt.so.0
%{_prefix}/lib/libghostty-vt.so.0.1.0

%{_prefix}/share/terminfo/x/xterm-ghostty
%if 0%{?fedora} < 42
    %{_prefix}/share/terminfo/g/ghostty
%endif

%files devel
%{_prefix}/include/ghostty/vt.h
%{_prefix}/include/ghostty/vt/
%{_prefix}/lib/libghostty-vt.so
%{_prefix}/share/pkgconfig/libghostty-vt.pc

%changelog
%autochangelog
