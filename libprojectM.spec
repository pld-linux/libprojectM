# TODO
# - cmake is borken and adds objects (static libs) in the middle of lists (Renderer/libRenderer.a):
#   Linking CXX shared library libprojectM.so
#   /usr/bin/cmake -E cmake_link_script CMakeFiles/projectM-shared.dir/link.txt --verbose=1
#   /usr/bin/ccache  i686-pld-linux-g++ -fPIC -O2 -fno-strict-aliasing -fwrapv -march=i686 -mtune=pentium4 -gdwarf-3 -g2   -fopenmp  -Wl,--as-needed -Wl,--no-copy-dt-needed-entries -Wl,-z,relro -Wl,-z,combreloc  -shared -Wl,-soname,libprojectM.so.2 -o libprojectM.so.2.0.1 CMakeFiles/projectM-shared.dir/projectM.cpp.o CMakeFiles/projectM-shared.dir/PCM.cpp.o CMakeFiles/projectM-shared.dir/Preset.cpp.o CMakeFiles/projectM-shared.dir/fftsg.cpp.o CMakeFiles/projectM-shared.dir/KeyHandler.cpp.o CMakeFiles/projectM-shared.dir/timer.cpp.o CMakeFiles/projectM-shared.dir/wipemalloc.cpp.o CMakeFiles/projectM-shared.dir/PresetLoader.cpp.o CMakeFiles/projectM-shared.dir/PresetChooser.cpp.o CMakeFiles/projectM-shared.dir/PipelineMerger.cpp.o CMakeFiles/projectM-shared.dir/ConfigFile.cpp.o CMakeFiles/projectM-shared.dir/TimeKeeper.cpp.o CMakeFiles/projectM-shared.dir/PresetFactory.cpp.o CMakeFiles/projectM-shared.dir/PresetFactoryManager.cpp.o Renderer/libRenderer.a NativePresetFactory/libNativePresetFactory.a MilkdropPresetFactory/libMilkdropPresetFactory.a -lGLEW -lftgl -lfreetype -lGLU -lGL -lSM -lICE -lX11 -lXext Renderer/libRenderer.a -lm
#
#   CMakeLists.txt having:
#   TARGET_LINK_LIBRARIES(projectM-shared ${PRESET_FACTORY_LINK_TARGETS} ${GLEW_LINK_TARGETS} m dl ${FTGL_LINK_TARGETS} ${OPENGL_LIBRARIES}  ${IMAGE_LINK_TARGETS} ${CG_LINK_TARGETS})
#
#   NativePresetFactory/CMakeLists.txt has:
#   TARGET_LINK_LIBRARIES(NativePresetFactory Renderer m)
#   which mixes .a between -l for dl

%define		pkgname	projectM
Summary:	Awesome music visualizer
Summary(pl.UTF-8):	Imponujący wizualizator muzyki
Name:		libprojectM
Version:	2.1.0
Release:	0.1
Epoch:		1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/project/projectm/%{version}/projectM-complete-%{version}-Source.tar.gz
# Source0-md5:	debf30f7ce94ff0102f06fbb0cc4e92b
Patch0:		paths.patch
Patch1:		pkgconfig.patch
Patch2:		c++14.patch
Patch3:		test-link.patch
URL:		http://projectm.sourceforge.net/
BuildRequires:	OpenGL-devel
BuildRequires:	cmake >= 2.6.0
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	ftgl-devel >= 2.1.3
BuildRequires:	gcc-c++ >= 6:4.2
BuildRequires:	glew-devel
BuildRequires:	libgomp-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.577
BuildRequires:	sed >= 4.0
Requires:	fonts-TTF-bitstream-vera
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# cmake (or cmake rules) are broken, mixes .a (objects) with libs (-l)
%define		filterout_ld	-Wl,--as-needed

%description
projectM is a reimplementation of Milkdrop under OpenGL. It is an
awesome music visualizer. There is nothing better in the world of
Unix.

%description -l pl.UTF-8
projectM jest reimplementacją projektu Milkdrop na OpenGL. Jest
imponującym wizualizatorem muzyki. Nie ma nic lepszego w świecie
uniksa.

%package devel
Summary:	Header files for projectM library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki projectM
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files for projectM library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki projectM.

%prep
%setup -q -n projectM-complete-%{version}-Source
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
install -d build
cd build
%cmake \
	-DCMAKE_LIB_DIR=%{_libdir} \
	-DprojectM_FONT_MENU="/usr/share/fonts/TTF/Vera.ttf" \
	-DprojectM_FONT_TITLE="/usr/share/fonts/TTF/VeraMono.ttf" \
	../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# COPYING is just license information, not actual LGPL text
%doc src/libprojectM/{COPYING,ChangeLog}
%attr(755,root,root) %{_libdir}/libprojectM.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libprojectM.so.2
%dir %{_datadir}/%{pkgname}
%{_datadir}/%{pkgname}/config.inp
%dir %{_datadir}/%{pkgname}/presets
%{_datadir}/%{pkgname}/presets/*.milk
%{_datadir}/%{pkgname}/presets/*.prjm
%{_datadir}/%{pkgname}/presets/*.tga
%dir %{_datadir}/%{pkgname}/shaders
%{_datadir}/%{pkgname}/shaders/*.cg

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libprojectM.so
%{_includedir}/%{name}
%{_pkgconfigdir}/libprojectM.pc
