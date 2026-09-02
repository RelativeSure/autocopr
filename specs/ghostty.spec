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

# zig build resolves ghostty's package dependencies (declared in
# build.zig.zon, including ones only reachable transitively) over the network
# via Zig's package manager, but %build runs in a network-isolated chroot. So
# every dependency zig would otherwise fetch is vendored below as its own
# Source and pre-seeded into Zig's global package cache in %prep, keyed by
# the content hash zig itself computes for that package. This list was
# derived by running the exact zig build invocation below, with network
# enabled, inside a chroot with this spec's BuildRequires installed, and
# recording every package it fetched.
Source3:        https://deps.files.ghostty.org/DearBindings_v0.17_ImGui_v1.92.5-docking.tar.gz
Source4:        https://github.com/ocornut/imgui/archive/refs/tags/v1.92.5-docking.tar.gz
Source5:        https://deps.files.ghostty.org/glslang-12201278a1a05c0ce0b6eb6026c65cd3e9247aa041b1c260324bf29cee559dd23ba1.tar.gz
Source6:        https://deps.files.ghostty.org/gobject-2025-11-08-23-1.tar.zst
Source7:        https://deps.files.ghostty.org/highway-66486a10623fa0d72fe91260f96c892e41aceb06.tar.gz
Source8:        https://deps.files.ghostty.org/ghostty-themes-release-20260216-151611-fc73ce3.tgz
Source9:        https://deps.files.ghostty.org/JetBrainsMono-2.304.tar.gz
Source10:       https://deps.files.ghostty.org/libpng-1220aa013f0c83da3fb64ea6d327f9173fa008d10e28bc9349eac3463457723b1c66.tar.gz
Source11:       https://deps.files.ghostty.org/libxev-34fa50878aec6e5fa8f532867001ab3c36fae23e.tar.gz
Source12:       https://deps.files.ghostty.org/NerdFontsSymbolsOnly-3.4.0.tar.gz
Source13:       https://deps.files.ghostty.org/oniguruma-1220c15e72eadd0d9085a8af134904d9a0f5dfcbed5f606ad60edc60ebeccd9706bb.tar.gz
Source14:       https://deps.files.ghostty.org/plasma_wayland_protocols-12207e0851c12acdeee0991e893e0132fc87bb763969a585dc16ecca33e88334c566.tar.gz
Source15:       https://deps.files.ghostty.org/spirv_cross-1220fb3b5586e8be67bc3feb34cbe749cf42a60d628d2953632c2f8141302748c8da.tar.gz
Source16:       https://deps.files.ghostty.org/utfcpp-1220d4d18426ca72fc2b7e56ce47273149815501d0d2395c2a98c726b31ba931e641.tar.gz
Source17:       https://deps.files.ghostty.org/uucode-0.2.0-ZZjBPqZVVABQepOqZHR7vV_NcaN-wats0IB6o-Exj6m9.tar.gz
Source18:       https://deps.files.ghostty.org/vaxis-7dbb9fd3122e4ffad262dd7c151d80d863b68558.tar.gz
Source19:       https://github.com/jacobsandlund/uucode/archive/5f05f8f83a75caea201f12cc8ea32a2d82ea9732.tar.gz
Source20:       https://deps.files.ghostty.org/wayland-9cb3d7aa9dc995ffafdbdef7ab86a949d0fb0e7d.tar.gz
Source21:       https://deps.files.ghostty.org/wayland-protocols-258d8f88f2c8c25a830c6316f87d23ce1a0f12d9.tar.gz
Source22:       https://deps.files.ghostty.org/pixels-12207ff340169c7d40c570b4b6a97db614fe47e0d83b5801a932dcd44917424c8806.tar.gz
Source23:       https://deps.files.ghostty.org/wuffs-122037b39d577ec2db3fd7b2130e7b69ef6cc1807d68607a7c232c958315d381b5cd.tar.gz
Source24:       https://deps.files.ghostty.org/z2d-0.10.0-j5P_Hu-6FgBsZNgwphIqh17jDnj8_yPtD8yzjO6PpHRQ.tar.gz
Source25:       https://deps.files.ghostty.org/zf-3c52637b7e937c5ae61fd679717da3e276765b23.tar.gz
Source26:       https://deps.files.ghostty.org/zig_wayland-1b5c038ec10da20ed3a15b0b2a6db1c21383e8ea.tar.gz
Source27:       https://github.com/ivanstepanovftw/zigimg/archive/d7b7ab0ba0899643831ef042bd73289510b39906.tar.gz
Source28:       https://deps.files.ghostty.org/zlib-1220fed0c74e1019b3ee29edae2051788b080cd96e90d56836eea857b0b966742efb.tar.gz

# Table of vendored zig dependencies: each SourceN's resolved path, its
# sha256 (verified in %prep before extraction), and the Zig package-cache
# hash it must be seeded under (~/.cache/zig/p/<hash>, i.e. what a live
# "zig build" would fetch it as). %{SOURCEn} is expanded here at spec-parse
# time since a shell loop over the source number can't build that macro name
# itself.
%global zig_deps_table %{SOURCE3} 8bfec500e00926f679853ee23d67cc392d3c3181733ca4704738651d3f70baa3 N-V-__8AANT61wB--nJ95Gj_ctmzAtcjloZ__hRqNw5lC1Kr \
%{SOURCE4} c816c20e8c75f3e15ae867350e79925502d1a6a85938bb1a73b8927e5f31f9cb N-V-__8AAEbOfQBnvcFcCX2W5z7tDaN8vaNZGamEQtNOe0UI \
%{SOURCE5} 14a2edbb509cb3e51a9a53e3f5e435dbf5971604b4b833e63e6076e8c0a997b5 N-V-__8AABzkUgISeKGgXAzgtutgJsZc0-kkeqBBscJgMkvy \
%{SOURCE6} d9bd4306f0081d8e4b848b6adfeabd2fab49822ee2b679eb4801dcedf5d60c48 gobject-0.3.0-Skun7ANLnwDvEfIpVmohcppXgOvg_I6YOJFmPIsKfXk- \
%{SOURCE7} 87d4f8893ef4e08f224973608ffebf94268a81380ba79c12e8841968c80aa212 N-V-__8AAGmZhABbsPJLfbqrh6JTHsXhY6qCaLAQyx25e0XE \
%{SOURCE8} 14200bb86a0c814ab69609d500b280b396b6d2eb835edf0676de4a789c0aa8fd N-V-__8AABVbAwBwDRyZONfx553tvMW8_A2OKUoLzPUSRiLF \
%{SOURCE9} c57a691e8b82ad098b5963f3959032e4038f391087af7715885ba59046105cc4 N-V-__8AAIC5lwAVPJJzxnCAahSvZTIlG-HhtOvnM1uh-66x \
%{SOURCE10} fecc95b46cf05e8e3fc8a414750e0ba5aad00d89e9fdf175e94ff041caf1a03a N-V-__8AAJrvXQCqAT8Mg9o_tk6m0yf5Fz-gCNEOKLyTSerD \
%{SOURCE11} 6003ea6b96e4a518a128f932327d79a11bd30996b13b73baeb29916379487dd7 libxev-0.0.0-86vtc4IcEwCqEYxEYoN_3KXmc6A9VLcm22aVImfvecYs \
%{SOURCE12} 1164d1b956d4bde248d7b2f0998c43cc94f5202431a1564a793895b1e73b0d04 N-V-__8AAMVLTABmYkLqhZPLXnMl-KyN38R8UVYqGrxqO26s \
%{SOURCE13} 001aa1202e78448f4c0bf1a48c76e556876b36f16d92ce3207eccfd61d99f2a0 N-V-__8AAHjwMQDBXnLq3Q2QhaivE0kE2aD138vtX2Bq1g7c \
%{SOURCE14} 5c58ba214acd8e6bca3426dc08b022c46a8dd997b29a1b3e28badf71c20df441 N-V-__8AAKYZBAB-CFHBKs3u4JkeiT4BMvyHu3Y5aaWF3Bbs \
%{SOURCE15} b52b6fcfc45e7fa69b1f06a1362c155473444e2cc09995556b156c53ba6657e3 N-V-__8AANb6pwD7O1WG6L5nvD_rNMvnSc9Cpg1ijSlTYywv \
%{SOURCE16} ffc668a310e77607d393f3c18b32715f223da1eac4c4d6e0579a11df8e6b59cf N-V-__8AAHffAgDU0YQmynL8K35WzkcnMUmBVQHQ0jlcKpjH \
%{SOURCE17} d0abee0f4f8bd6eae3c051777e16e7c42d8964aaaa015591c4e565703f465f95 uucode-0.2.0-ZZjBPqZVVABQepOqZHR7vV_NcaN-wats0IB6o-Exj6m9 \
%{SOURCE18} 2e72332bc89c5b541ec6e6bd48769e1f3fb757c4006f3d1af940b54f9b088ef6 vaxis-0.5.1-BWNV_LosCQAGmCCNOLljCIw6j6-yt53tji6n6rwJ2BhS \
%{SOURCE19} 40b90ae087e26546a57961c40ae0cae1926d94140502bafd0f551db9de66e62a uucode-0.1.0-ZZjBPj96QADXyt5sqwBJUnhaDYs_qBeeKijZvlRa0eqM \
%{SOURCE20} ea4191d68e437677e51f3aacde27829810144e931d397a327dc6035e2c39c50d N-V-__8AAKrHGAAs2shYq8UkE6bGcR1QJtLTyOE_lcosMn6t \
%{SOURCE21} 5cedcadde81b75e60f23e5e83b5dd2b8eb4efb9f8f79bd7a347d148aeb0530f8 N-V-__8AAKw-DAAaV8bOAAGqA0-oD7o-HNIlPFYKRXSPT03S \
%{SOURCE22} 55e83b16d091082502bf149bf457f31f42092c5982650e3ffbae7b48871bf11a N-V-__8AADYiAAB_80AWnH1AxXC0tql9thT-R-DYO1gBqTLc \
%{SOURCE23} 9e4cd20abe96e6c4c6ede9c3057108860126e7be2e2c3e35515476c250be1c13 N-V-__8AAAzZywE3s51XfsLbP9eyEw57ae9swYB9aGB6fCMs \
%{SOURCE24} 69f21da2efd5ee0937fe55c4d09e48afc4fb2f91a01ef167c8c275ae046797f7 z2d-0.10.0-j5P_Hu-6FgBsZNgwphIqh17jDnj8_yPtD8yzjO6PpHRQ \
%{SOURCE25} 3b015d928af04e9e26272bc15eb4dbb4d9a9d469eb6d290a0ddae673b77c4568 zf-0.10.3-OIRy8RuJAACKA3Lohoumrt85nRbHwbpMcUaLES8vxDnh \
%{SOURCE26} 4f146b735ed0d527f520e3bf71d3e93f72c3d0fa583ae8edd3a4851f7079124e wayland-0.5.0-dev-lQa1khrMAQDJDwYFKpdH3HizherB7sHo5dKMECfvxQHe \
%{SOURCE27} 2c1ed76ba2b35514544b0c27c9633ecba7c31be9080e37e7a010c93b5a1bc553 zigimg-0.1.0-8_eo2vHnEwCIVW34Q14Ec-xUlzIoVg86-7FU2ypPtxms \
%{SOURCE28} 17e88863f3600672ab49182f217281b6fc4d3c762bde361935e436a95214d05c N-V-__8AAB0eQwD-0MdOEBmz7intriBReIsIDNlukNVoNu6o

Name:           ghostty
Version:        1.3.1
Release:        7%{?dist}
Summary:        Fast, feature-rich, cross-platform terminal emulator

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
BuildRequires: zstd

Requires: fontconfig
Requires: freetype
Requires: gtk4
Requires: harfbuzz
Requires: oniguruma
Requires: pixman
Requires: zlib-ng

%description
%{summary},
using platform-native UI and GPU acceleration.

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

# Seed Zig's global package cache with the vendored dependencies so the
# offline "zig build" in %build finds every dependency already fetched
# instead of reaching out to the network. The table is read from a heredoc
# (rather than shell positional args) so it doesn't matter whether the
# newlines in the macro's expansion survive as real shell line breaks.
export ZIG_GLOBAL_CACHE_DIR=%{_builddir}/zig-global-cache
mkdir -p "$ZIG_GLOBAL_CACHE_DIR/p"
while read -r src sum zighash; do
    [ -n "$src" ] || continue
    echo "${sum}  ${src}" | sha256sum -c -
    destdir="$ZIG_GLOBAL_CACHE_DIR/p/${zighash}"
    mkdir -p "$destdir"
    case "$src" in
        *.tar.zst) tar --use-compress-program=unzstd -xf "$src" -C "$destdir" --strip-components=1 ;;
        *)         tar -xf "$src" -C "$destdir" --strip-components=1 ;;
    esac
done <<'ZIG_DEPS_EOF'
%{zig_deps_table}
ZIG_DEPS_EOF

%build
export PATH="%{_builddir}/zig-toolchain:$PATH"
export ZIG_GLOBAL_CACHE_DIR=%{_builddir}/zig-global-cache

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

# An %install section would run against a freshly-emptied %%{buildroot}
# (rpm always clears it first), wiping out the DESTDIR install this
# %%build already did above (zig build doesn't cleanly separate a build
# step from a DESTDIR-install step) - so %%find_lang runs here instead,
# against the real populated buildroot, and %%install is intentionally
# omitted.
%find_lang com.mitchellh.ghostty

%files -f com.mitchellh.ghostty.lang
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
