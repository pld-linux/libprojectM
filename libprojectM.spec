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
Version:	2.0.1
Release:	4
Epoch:		1
License:	LGPL
Group:		Libraries
Source0:	http://downloads.sourceforge.net/project/projectm/%{version}/projectM-%{version}-Source.tar.gz
# Source0-md5:	f8bf795878cdbbef54784cf2390b4c89
Patch0:		%{name}-soname.patch
Patch1:		%{name}-fonts.patch
Patch2:		%{name}-static.patch
Patch3:		as-needed.patch
Patch4:		%{name}-pkgconfig.patch
Patch5:		01-change-texture-size.patch
Patch6:		04-change-preset-duration.patch
Patch7:		06-fix-numeric-locale.patch
URL:		http://projectm.sourceforge.net/
BuildRequires:	cmake
BuildRequires:	ftgl-devel >= 2.1.3
BuildRequires:	glew-devel
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

%package static
Summary:	Static projectM library
Summary(pl.UTF-8):	Statyczna biblioteka projectM
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static projectM library.

%description static -l pl.UTF-8
Statyczna biblioteka projectM.

%prep
%setup -q -n projectM-%{version}-Source
%undos config.inp.in
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4	-p1
%patch5	-p0
%patch6	-p0
%patch7	-p0

%build
install -d build
cd build
%cmake \
	-DCMAKE_LIB_DIR=%{_libdir} \
	-DBUILD_PROJECTM_STATIC=yes \
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
%doc ChangeLog
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

%files static
%defattr(644,root,root,755)
%{_libdir}/libprojectM.a
