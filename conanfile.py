#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import platform
import shutil

from conans import ConanFile, AutoToolsBuildEnvironment, tools


# noinspection PyUnresolvedReferences
class FFmpegConan(ConanFile):
    name = "ffmpeg"
    version = "4.1.3"
    url = "https://github.com/MX-Dev/conan-ffmpeg"
    description = "A complete, cross-platform solution to record, convert and stream audio and video"
    # https://github.com/FFmpeg/FFmpeg/blob/master/LICENSE.md
    license = "LGPL-2.1-or-later", "GPL-2.0-or-later"
    homepage = "https://ffmpeg.org/"
    author = "Bincrafters <bincrafters@gmail.com>"
    topics = "ffmpeg", "multimedia", "audio", "video", "encoder", "decoder", "encoding", "decoding", \
             "transcoding", "multiplexer", "demultiplexer", "streaming"
    _source_subfolder = "sources"
    exports_sources = ["LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "disable_filters": [True, False],
               "disable_bsfs": [True, False],
               "disable_parsers": [True, False],
               "disable_muxers": [True, False],
               "disable_demuxers": [True, False],
               "disable_protocols": [True, False],
               "disable_encoders": [True, False],
               "disable_decoders": [True, False],
               "disable_devices": [True, False],
               "disable_hwaccel": [True, False],
               "postproc": [True, False],
               "avdevice": [True, False],
               "cuda": [True, False],
               "cuvid": [True, False],
               "zlib": [True, False],
               "bzlib": [True, False],
               "lzma": [True, False],
               "iconv": [True, False],
               "freetype": [True, False],
               "openjpeg": [True, False],
               "openh264": [True, False],
               "opus": [True, False],
               "vorbis": [True, False],
               "zmq": [True, False],
               "sdl2": [True, False],
               "x264": [True, False],
               "x265": [True, False],
               "vpx": [True, False],
               "mp3lame": [True, False],
               "fdk_aac": [True, False],
               "webp": [True, False],
               "openssl": [True, False],
               "alsa": [True, False],
               "pulse": [True, False],
               "vaapi": [True, False],
               "vdpau": [True, False],
               "xcb": [True, False],
               "appkit": [True, False],
               "avfoundation": [True, False],
               "coreimage": [True, False],
               "audiotoolbox": [True, False],
               "videotoolbox": [True, False],
               "securetransport": [True, False],
               "qsv": [True, False],
               "jni": [True, False],
               "mediacodec": [True, False]}
    default_options = ("shared=False",
                       "fPIC=True",
                       "disable_filters=False",
                       "disable_bsfs=False",
                       "disable_parsers=False",
                       "disable_muxers=False",
                       "disable_demuxers=False",
                       "disable_protocols=False",
                       "disable_encoders=False",
                       "disable_decoders=False",
                       "disable_devices=False",
                       "disable_hwaccel=False",
                       "postproc=False",
                       "avdevice=False",
                       "cuda=False",
                       "cuvid=False",
                       "zlib=False",
                       "bzlib=False",
                       "lzma=False",
                       "iconv=False",
                       "freetype=False",
                       "openjpeg=False",
                       "openh264=False",
                       "openssl=False",
                       "opus=False",
                       "vorbis=False",
                       "zmq=False",
                       "sdl2=False",
                       "x264=False",
                       "x265=False",
                       "vpx=False",
                       "mp3lame=False",
                       "fdk_aac=False",
                       "webp=False",
                       "alsa=False",
                       "pulse=False",
                       "vaapi=False",
                       "vdpau=False",
                       "xcb=False",
                       "appkit=False",
                       "avfoundation=False",
                       "coreimage=False",
                       "audiotoolbox=False",
                       "videotoolbox=False",
                       "securetransport=False",
                       "qsv=False",
                       "jni=True",
                       "mediacodec=True")

    @property
    def _is_windows_host(self):
        return platform.system() == "Windows"

    @property
    def _is_linux_host(self):
        return platform.system() == "Linux"

    @property
    def _is_mac_host(self):
        return platform.system() == "Darwin"

    @property
    def _is_mingw_windows(self):
        return self._is_windows_host and self.settings.compiler == 'gcc' and os.name == 'nt'

    @property
    def _is_msvc(self):
        return self.settings.compiler == 'Visual Studio'

    @property
    def _is_android_cross(self):
        return self.settings.os == 'Android' and self.settings.compiler == 'clang'

    def source(self):
        git = tools.Git(folder=self._source_subfolder)
        git.clone("https://github.com/FFmpeg/FFmpeg.git", "release/4.1")

    def configure(self):
        del self.settings.compiler.libcxx

    def config_options(self):
        if self._is_android_cross:
            api_level = int(str(self.settings.os.api_level))
            if api_level > 21:
                raise Exception("Android builds require API Level <= 21")

        if self.settings.os == "Windows":
            del self.options.fPIC
        if not self._is_linux_host or self._is_android_cross:
            self.options.remove("vaapi")
            self.options.remove("vdpau")
            self.options.remove("xcb")
            self.options.remove("alsa")
            self.options.remove("pulse")
        if not self._is_mac_host or self._is_android_cross:
            self.options.remove("appkit")
            self.options.remove("avfoundation")
            self.options.remove("coreimage")
            self.options.remove("audiotoolbox")
            self.options.remove("videotoolbox")
            self.options.remove("securetransport")
        if not self._is_windows_host or self._is_android_cross:
            self.options.remove("qsv")
        if not self._is_android_cross:
            self.options.remove("jni")
            self.options.remove("mediacodec")

    def build_requirements(self):
        self.build_requires("yasm_installer/1.3.0@bincrafters/stable")
        if self._is_windows_host:
            self.build_requires("msys2_installer/latest@bincrafters/stable")

    def requirements(self):
        if self.options.zlib:
            self.requires.add("zlib/1.2.11@conan/stable")
        if self.options.bzlib:
            self.requires.add("bzip2/1.0.6@conan/stable")
        if self.options.lzma:
            self.requires.add("lzma/5.2.3@bincrafters/stable")
        if self.options.iconv:
            self.requires.add("libiconv/1.15@bincrafters/stable")
        if self.options.freetype:
            self.requires.add("freetype/2.9.0@bincrafters/stable")
        if self.options.openjpeg:
            self.requires.add("openjpeg/2.3.0@bincrafters/stable")
        if self.options.openh264:
            self.requires.add("openh264/1.7.0@bincrafters/stable")
        if self.options.vorbis:
            self.requires.add("vorbis/1.3.6@bincrafters/stable")
        if self.options.opus:
            self.requires.add("opus/1.2.1@bincrafters/stable")
        if self.options.zmq:
            self.requires.add("zmq/4.2.2@bincrafters/stable")
        if self.options.sdl2:
            self.requires.add("sdl2/2.0.7@bincrafters/stable")
        if self.options.x264:
            self.requires.add("libx264/20171211@bincrafters/stable")
        if self.options.x265:
            self.requires.add("libx265/2.7@bincrafters/stable")
        if self.options.vpx:
            self.requires.add("libvpx/1.7.0@bincrafters/stable")
        if self.options.mp3lame:
            self.requires.add("libmp3lame/3.100@bincrafters/stable")
        if self.options.fdk_aac:
            self.requires.add("libfdk_aac/0.1.5@bincrafters/stable")
        if self.options.webp:
            self.requires.add("libwebp/1.0.0@bincrafters/stable")
        if self.options.openssl:
            self.requires.add("OpenSSL/1.1.1b@conan/stable")
        if self._is_windows_host and not self._is_android_cross:
            if self.options.qsv:
                self.requires.add("intel_media_sdk/2018R2@bincrafters/stable")

    def system_requirements(self):
        if self.options.alsa or self.options.pulse or self.options.vaapi or self.options.vdpau or self.options.xcb:
            if self._is_linux_host and tools.os_info.is_linux and not self._is_android_cross:
                if tools.os_info.with_apt:
                    installer = tools.SystemPackageTool()
                    arch_suffix = ''
                    if self.settings.arch == "x86":
                        arch_suffix = ':i386'
                    elif self.settings.arch == "x86_64":
                        arch_suffix = ':amd64'

                    packages = ['pkg-config']
                    if self.options.alsa:
                        packages.append('libasound2-dev%s' % arch_suffix)
                    if self.options.pulse:
                        packages.append('libpulse-dev%s' % arch_suffix)
                    if self.options.vaapi:
                        packages.append('libva-dev%s' % arch_suffix)
                    if self.options.vdpau:
                        packages.append('libvdpau-dev%s' % arch_suffix)
                    if self.options.xcb:
                        packages.extend(['libxcb1-dev%s' % arch_suffix,
                                         'libxcb-shm0-dev%s' % arch_suffix,
                                         'libxcb-shape0-dev%s' % arch_suffix,
                                         'libxcb-xfixes0-dev%s' % arch_suffix])
                    for package in packages:
                        installer.install(package)

    def _copy_pkg_config(self, name):
        root = self.deps_cpp_info[name].rootpath
        pc_dir = os.path.join(root, 'lib', 'pkgconfig')
        pc_files = glob.glob('%s/*.pc' % pc_dir)
        for pc_name in pc_files:
            new_pc = os.path.join('pkgconfig', os.path.basename(pc_name))
            self.output.warn('copy .pc file %s' % os.path.basename(pc_name))
            shutil.copy(pc_name, new_pc)
            prefix = tools.unix_path(root) if self._is_windows_host else root
            tools.replace_prefix_in_pc_file(new_pc, prefix)

    def _patch_sources(self):
        if self._is_msvc and self.options.x264 and not self.options['x264'].shared:
            # suppress MSVC linker warnings: https://trac.ffmpeg.org/ticket/7396
            # warning LNK4049: locally defined symbol x264_levels imported
            # warning LNK4049: locally defined symbol x264_bit_depth imported
            tools.replace_in_file(os.path.join(self._source_subfolder, 'libavcodec', 'libx264.c'),
                                  '#define X264_API_IMPORTS 1', '')
        if self.options.openssl:
            # https://trac.ffmpeg.org/ticket/5675
            openssl_libraries = ' '.join(['-l%s' % lib for lib in self.deps_cpp_info["OpenSSL"].libs])
            tools.replace_in_file(os.path.join(self._source_subfolder, 'configure'),
                                  'check_lib openssl openssl/ssl.h SSL_library_init -lssl -lcrypto -lws2_32 -lgdi32 ||',
                                  'check_lib openssl openssl/ssl.h OPENSSL_init_ssl %s || ' % openssl_libraries)

    def build(self):
        self._patch_sources()
        if self._is_windows_host:
            msys_bin = self.deps_env_info['msys2_installer'].MSYS_BIN
            with tools.environment_append({'PATH': [msys_bin],
                                           'CONAN_BASH_PATH': os.path.join(msys_bin, 'bash.exe')}):
                if self._is_msvc:
                    with tools.vcvars(self.settings):
                        self.build_configure()
                else:
                    self.build_configure()
        else:
            self.build_configure()

    def build_configure(self):
        with tools.chdir(self._source_subfolder):
            prefix = tools.unix_path(self.package_folder) if self._is_windows_host else self.package_folder
            args = ['--prefix=%s' % prefix,
                    '--disable-doc',
                    '--disable-programs']
            if self.options.shared:
                args.extend(['--disable-static', '--enable-shared'])
            else:
                args.extend(['--disable-shared', '--enable-static'])
            args.append('--pkg-config-flags=--static')
            if self.settings.build_type == 'Debug':
                args.extend(['--disable-optimizations', '--disable-mmx', '--disable-stripping', '--enable-debug'])
            if self._is_msvc:
                args.append('--toolchain=msvc')
                args.append('--extra-cflags=-%s' % self.settings.compiler.runtime)
                if int(str(self.settings.compiler.version)) <= 12:
                    # Visual Studio 2013 (and earlier) doesn't support "inline" keyword for C (only for C++)
                    args.append('--extra-cflags=-Dinline=__inline' % self.settings.compiler.runtime)

            if self.settings.arch == 'x86' or self._is_android_cross:
                args.append('--arch=%s' % {"armv7": "arm", "armv8": "arm64"}
                            .get(str(self.settings.arch), str(self.settings.arch)))

            if self.settings.os != "Windows":
                args.append('--enable-pic' if self.options.fPIC else '--disable-pic')
            if self.options.disable_filters:
                args.append('--disable-filters')
            if self.options.disable_bsfs:
                args.append('--disable-bsfs')
            if self.options.disable_parsers:
                args.append('--disable-parsers')
            if self.options.disable_muxers:
                args.append('--disable-muxers')
            if self.options.disable_demuxers:
                args.append('--disable-demuxers')
            if self.options.disable_protocols:
                args.append('--disable-protocols')
            if self.options.disable_encoders:
                args.append('--disable-encoders')
            if self.options.disable_decoders:
                args.append('--disable-decoders')
            if self.options.disable_devices:
                args.append('--disable-devices')
            if self.options.disable_hwaccel:
                args.append('--disable-hwaccels')

            args.append('--enable-postproc' if self.options.postproc else '--disable-postproc')
            args.append('--enable-avdevice' if self.options.avdevice else '--disable-avdevice')
            args.append('--enable-zlib' if self.options.zlib else '--disable-zlib')
            args.append('--enable-bzlib' if self.options.bzlib else '--disable-bzlib')
            args.append('--enable-lzma' if self.options.lzma else '--disable-lzma')
            args.append('--enable-iconv' if self.options.iconv else '--disable-iconv')
            args.append('--enable-libfreetype' if self.options.freetype else '--disable-libfreetype')
            args.append('--enable-libopenjpeg' if self.options.openjpeg else '--disable-libopenjpeg')
            args.append('--enable-libopenh264' if self.options.openh264 else '--disable-libopenh264')
            args.append('--enable-libvorbis' if self.options.vorbis else '--disable-libvorbis')
            args.append('--enable-libopus' if self.options.opus else '--disable-libopus')
            args.append('--enable-libzmq' if self.options.zmq else '--disable-libzmq')
            args.append('--enable-sdl2' if self.options.sdl2 else '--disable-sdl2')
            args.append('--enable-libx264' if self.options.x264 else '--disable-libx264')
            args.append('--enable-libx265' if self.options.x265 else '--disable-libx265')
            args.append('--enable-libvpx' if self.options.vpx else '--disable-libvpx')
            args.append('--enable-libmp3lame' if self.options.mp3lame else '--disable-libmp3lame')
            args.append('--enable-libfdk-aac' if self.options.fdk_aac else '--disable-libfdk-aac')
            args.append('--enable-libwebp' if self.options.webp else '--disable-libwebp')
            args.append('--enable-openssl' if self.options.openssl else '--disable-openssl')
            args.append('--enable-cuda' if self.options.cuda else '--disable-cuda')
            args.append('--enable-cuvid' if self.options.cuvid else '--disable-cuvid')

            if self.options.x264 or self.options.x265 or self.options.postproc:
                args.append('--enable-gpl')

            if self.options.fdk_aac:
                args.append('--enable-nonfree')

            if self._is_android_cross:
                args.append('--enable-mediacodec' if self.options.mediacodec else '--disable-mediacodec')
                args.append('--enable-jni' if self.options.jni else '--disable-jni')
                args.extend(['--target-os=android',
                             '--enable-cross-compile',
                             '--disable-symver'])

                if os.getenv("CC"):
                    args.append("--cc=%s" % os.getenv("CC"))
                if os.getenv("CXX"):
                    args.append("--cxx=%s" % os.getenv("CXX"))
                if os.getenv("CCAS"):
                    args.append("--as=%s" % os.getenv("CCAS"))
                if os.getenv("AR"):
                    args.append("--ar=%s" % os.getenv("AR"))
                if os.getenv("LD"):
                    args.append("--ld=%s" % os.getenv("LD"))
                if os.getenv("STRIP"):
                    args.append("--strip=%s" % os.getenv("STRIP"))
                if os.getenv("NM"):
                    args.append("--nm=%s" % os.getenv("NM"))
                if os.getenv("RANLIB"):
                    args.append("--ranlib=%s" % os.getenv("RANLIB"))
                if self.settings.arch == "armv7":
                    args.extend(['--cpu=armv7-a', '--disable-inline-asm'])
                # text segment is not shareable
                if self.settings.arch == "x86":
                    args.append('--disable-asm')

                extra_cflags = []
                if os.getenv("CFLAGS"):
                    extra_cflags.append(os.getenv("CFLAGS"))

                args.append("--extra-cflags=%s" % " ".join(extra_cflags))

            else:
                if self._is_linux_host:
                    args.append('--enable-alsa' if self.options.alsa else '--disable-alsa')
                    args.append('--enable-libpulse' if self.options.pulse else '--disable-libpulse')
                    args.append('--enable-vaapi' if self.options.vaapi else '--disable-vaapi')
                    args.append('--enable-vdpau' if self.options.vdpau else '--disable-vdpau')
                    if self.options.xcb:
                        args.extend(['--enable-libxcb', '--enable-libxcb-shm',
                                     '--enable-libxcb-shape', '--enable-libxcb-xfixes'])
                    else:
                        args.extend(['--disable-libxcb', '--disable-libxcb-shm',
                                     '--disable-libxcb-shape', '--disable-libxcb-xfixes'])

                if self._is_mac_host:
                    args.append('--enable-appkit' if self.options.appkit else '--disable-appkit')
                    args.append('--enable-avfoundation' if self.options.avfoundation else '--disable-avfoundation')
                    args.append('--enable-coreimage' if self.options.avfoundation else '--disable-coreimage')
                    args.append('--enable-audiotoolbox' if self.options.audiotoolbox else '--disable-audiotoolbox')
                    args.append('--enable-videotoolbox' if self.options.videotoolbox else '--disable-videotoolbox')
                    args.append('--enable-securetransport' if self.options.securetransport else '--disable-securetransport')

                if self._is_windows_host:
                    args.append('--enable-libmfx' if self.options.qsv else '--disable-libmfx')

            os.makedirs('pkgconfig')
            if self.options.freetype:
                self._copy_pkg_config('freetype')
                self._copy_pkg_config('libpng')
            if self.options.opus:
                self._copy_pkg_config('opus')
            if self.options.vorbis:
                self._copy_pkg_config('ogg')
                self._copy_pkg_config('vorbis')
            if self.options.zmq:
                self._copy_pkg_config('zmq')
            if self.options.sdl2:
                self._copy_pkg_config('sdl2')
            if self.options.x264:
                self._copy_pkg_config('libx264')
            if self.options.x265:
                self._copy_pkg_config('libx265')
            if self.options.vpx:
                self._copy_pkg_config('libvpx')
            if self.options.fdk_aac:
                self._copy_pkg_config('libfdk_aac')
            if self.options.openh264:
                self._copy_pkg_config('openh264')
            if self.options.openjpeg:
                self._copy_pkg_config('openjpeg')
            if self.options.webp:
                self._copy_pkg_config('libwebp')

            pkg_config_path = os.path.abspath('pkgconfig')
            pkg_config_path = tools.unix_path(pkg_config_path) if self._is_windows_host else pkg_config_path

            try:
                if self._is_windows_host:
                    # hack for MSYS2 which doesn't inherit PKG_CONFIG_PATH
                    for filename in ['.bashrc', '.bash_profile', '.profile']:
                        tools.run_in_windows_bash(self, 'cp ~/%s ~/%s.bak' % (filename, filename))
                        command = 'echo "export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%s" >> ~/%s' \
                                  % (pkg_config_path, filename)
                        tools.run_in_windows_bash(self, command)

                if self._is_android_cross:
                    env_make = os.getenv('CONAN_MAKE_PROGRAM')
                    make = str(env_make) if env_make and "make" in str(
                        env_make) else "make.exe" if self._is_windows_host else "make"
                    os.environ['CONAN_MAKE_PROGRAM'] = make

                env_build = AutoToolsBuildEnvironment(self, win_bash=self._is_windows_host)
                # ffmpeg's configure is not actually from autotools, so it doesn't understand standard options like
                # --host, --build, --target
                env_build.configure(args=args, build=False, host=False, target=False, pkg_config_paths=[pkg_config_path])
                env_build.make()
                env_build.make(args=['install'])
            finally:
                if self._is_windows_host:
                    for filename in ['.bashrc', '.bash_profile', '.profile']:
                        tools.run_in_windows_bash(self, 'cp ~/%s.bak ~/%s' % (filename, filename))
                        tools.run_in_windows_bash(self, 'rm -f ~/%s.bak' % filename)

    def package(self):
        with tools.chdir(self._source_subfolder):
            self.copy(pattern="LICENSE")
        if self._is_msvc and not self.options.shared:
            # ffmpeg produces .a files which are actually .lib files
            with tools.chdir(os.path.join(self.package_folder, 'lib')):
                libs = glob.glob('*.a')
                for lib in libs:
                    shutil.move(lib, lib[:-2] + '.lib')

    def package_info(self):
        libs = ['avfilter', 'avformat', 'avcodec', 'swresample', 'swscale', 'avutil']
        if self.options.postproc:
            libs.append('postproc')
        if self.options.avdevice:
            libs.append('avdevice')
        if self._is_msvc:
            if self.options.shared:
                self.cpp_info.libs = libs
                self.cpp_info.libdirs.append('bin')
            else:
                self.cpp_info.libs = ['lib' + lib for lib in libs]
        else:
            self.cpp_info.libs = libs

        if not self._is_android_cross:
            if self._is_mac_host:
                frameworks = ['CoreVideo', 'CoreMedia', 'CoreGraphics', 'CoreFoundation', 'OpenGL', 'Foundation']
                if self.options.appkit:
                    frameworks.append('AppKit')
                if self.options.avfoundation:
                    frameworks.append('AVFoundation')
                if self.options.coreimage:
                    frameworks.append('CoreImage')
                if self.options.audiotoolbox:
                    frameworks.append('AudioToolbox')
                if self.options.videotoolbox:
                    frameworks.append('VideoToolbox')
                if self.options.securetransport:
                    frameworks.append('Security')
                for framework in frameworks:
                    self.cpp_info.exelinkflags.append("-framework %s" % framework)
                self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
            elif self._is_linux_host:
                self.cpp_info.libs.extend(['dl', 'pthread'])
                if self.options.alsa:
                    self.cpp_info.libs.append('asound')
                if self.options.pulse:
                    self.cpp_info.libs.append('pulse')
                if self.options.vaapi:
                    self.cpp_info.libs.extend(['va', 'va-drm', 'va-x11'])
                if self.options.vdpau:
                    self.cpp_info.libs.extend(['vdpau', 'X11'])
                if self.options.xcb:
                    self.cpp_info.libs.extend(['xcb', 'xcb-shm', 'xcb-shape', 'xcb-xfixes'])
            elif self._is_windows_host:
                self.cpp_info.libs.extend(['ws2_32', 'secur32', 'shlwapi', 'strmiids', 'vfw32', 'bcrypt'])

        if self.settings.os != "Windows" and self.options.fPIC:
            # https://trac.ffmpeg.org/ticket/1713
            # https://ffmpeg.org/platform.html#Advanced-linking-configuration
            # https://ffmpeg.org/pipermail/libav-user/2014-December/007719.html
            self.cpp_info.sharedlinkflags.append("-Wl,-Bsymbolic")
