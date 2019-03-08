[settings]
compiler=clang
compiler.libcxx=libc++
compiler.version=8
os=Android
os.api_level=21
os_build=Windows
arch_build=x86_64
arch=armv7
build_type=Debug

[options]
ffmpeg:lzma=False
ffmpeg:opus=False
ffmpeg:zmq=False
ffmpeg:iconv=False
ffmpeg:openjpeg=False
ffmpeg:openh264=False
ffmpeg:x264=False
ffmpeg:x265=False
ffmpeg:postproc=False
ffmpeg:avdevice=False
ffmpeg:freetype=False
ffmpeg:vpx=False
ffmpeg:mp3lame=False
ffmpeg:fdk_aac=False
ffmpeg:webp=False
ffmpeg:mediacodec=False
ffmpeg:jni=False

[build_requires]
*: android-ndk/r19b@magix/testing