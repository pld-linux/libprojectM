#
# Conditional build:
%bcond_with	cg	# CG for Pixel Shader support
%bcond_with	devil	# DevIL instead of builtin SOIL for image loading
%bcond_without	jack	# JACK plugin
%bcond_without	openmp	# OpenMP for multi-core parallelization
%bcond_with	xmms	# XMMS plugin (deprecated; wants libxmms.pc, which is not provided)

%define		pkgname	projectM
Summary:	Awesome music visualizer
Summary(pl.UTF-8):	Imponujący wizualizator muzyki
Name:		libprojectM
Version:	2.1.0
Release:	3
Epoch:		1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/projectm/projectM-complete-%{version}-Source.tar.gz
# Source0-md5:	debf30f7ce94ff0102f06fbb0cc4e92b
Patch0:		paths.patch
Patch1:		pkgconfig.patch
Patch2:		c++14.patch
Patch3:		test-link.patch
URL:		http://projectm.sourceforge.net/
%{?with_DevIL:BuildRequires:	DevIL-devel}
%{?with_DevIL:BuildRequires:	DevIL-ILUT-devel}
BuildRequires:	OpenGL-devel
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtGui-devel >= 4
BuildRequires:	QtOpenGL-devel >= 4
BuildRequires:	QtXml-devel >= 4
BuildRequires:	SDL-devel
%{?with_cg:BuildRequires:	cg-devel}
BuildRequires:	cmake >= 2.8.0
BuildRequires:	desktop-file-utils
BuildRequires:	freetype-devel >= 1:2.3.5
BuildRequires:	ftgl-devel >= 2.1.3
BuildRequires:	glew-devel >= 1.4.0
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel}
%{?with_openmp:BuildRequires:	libgomp-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	libvisual-devel >= 0.4.0
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel >= 0.9.8
BuildRequires:	rpmbuild(macros) >= 1.605
%{?with_xmms:BuildRequires:	xmms-devel}
Requires:	fonts-TTF-bitstream-vera
Requires:	ftgl-devel >= 2.1.3
Requires:	glew-devel >= 1.4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package qt
Summary:	The Qt frontend to the projectM visualization library
Summary(pl.UTF):	Graficzny interfejs Qt do biblioteki wizualizacyjnej projectM
Group:		X11/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description qt
projectM-qt is a GUI designed to enhance the projectM user and preset
writer experience. It provides a way to browse, search, rate presets
and setup preset playlists for jack-projectM and pulseaudio-projectM.

%description qt -l pl.UTF-8
projectM-qt to graficzny interfejs użytkownika, mający poprawić
doznania użytkownika oraz piszącego ustawienia projectM. Daje
możliwość przeglądania, wyszukiwania, ustawiania współczynników oraz
predefiniowanych list odtwarzania dla wtyczek jack-projectM oraz
pulseaudio-projectM.

%package qt-devel
Summary:	Header files for projectM Qt library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki projectM Qt
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Requires:	%{name}-qt = %{epoch}:%{version}-%{release}
Requires:	QtCore-devel >= 4
Requires:	QtGui-devel >= 4
Requires:	QtOpenGL-devel >= 4
Requires:	QtXml-devel >= 4

%description qt-devel
Header files for projectM Qt library.

%description qt-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki projectM Qt.

%package -n jack-projectM
Summary:	The projectM visualization plugin for JACK
Summary(pl.UTF-8):	Wtyczka wizualizacji dla JACK-a
License:	GPLv2+ and MIT
Group:		Applications/Multimedia
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name}-qt = %{epoch}:%{version}-%{release}

%description -n jack-projectM
This package allows the use of the projectM visualization plugin
through any JACK compatible applications.

%description -n jack-projectM -l pl.UTF-8
Ten pakiet pozwala na używanie wtyczki wizualizacji projectM we
wszystkich aplikacjach wykorzystujących system dźwięku JACK.

%package -n pulseaudio-projectM
Summary:	The projectM visualization plugin for pulseaudio
Summary(pl.UTF-8):	Wtyczka wizualizacji dla pulseaudio
Group:		Applications/Multimedia
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name}-qt = %{epoch}:%{version}-%{release}
Requires:	pulseaudio-libs >= 0.9.8

%description -n pulseaudio-projectM
This package allows the use of the projectM visualization plugin
through any pulseaudio compatible applications.

%description -n pulseaudio-projectM -l pl.UTF-8
Ten pakiet pozwala na używanie wtyczki wizualizacji projectM we
wszystkich aplikacjach wykorzystujących system dźwięku pulseaudio.

%package -n libvisual-projectM
Summary:	ProjectM plugin for libvisual
Summary(pl.UTF-8):	Wtyczka ProjectM dla libvisual
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libvisual >= 0.4

%description -n libvisual-projectM
projectM is a reimplementation of Milkdrop under OpenGL. This is a
plugin for libvisual visualization library.

%description -n libvisual-projectM -l pl.UTF-8
projectM jest reimplementacją projektu Milkdrop na OpenGL. Ten pakiet
zawiera wtyczkę dla biblioteki wizualizacji libvisual.

%prep
%setup -q -n projectM-complete-%{version}-Source
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1

%build
install -d build
cd build
%cmake \
	-DCMAKE_LIB_DIR=%{_libdir} \
	-DprojectM_FONT_MENU="/usr/share/fonts/TTF/Vera.ttf" \
	-DprojectM_FONT_TITLE="/usr/share/fonts/TTF/VeraMono.ttf" \
	%{?with_jack:-DINCLUDE-PROJECTM-JACK=ON} \
	-DINCLUDE-PROJECTM-LIBVISUAL-ALSA=ON \
	-DINCLUDE-PROJECTM-TEST=OFF \
	%{?with_xmms:-DINCLUDE-PROJECTM-XMMS=ON} \
	%{?with_cg:-DUSE_CG=ON} \
	%{?with_devil:-DUSE_DEVIL=ON} \
	%{!?with_openmp:-DUSE_OPENMP=OFF} \
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# omitted by CMakeLists.txt
install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -p src/projectM-jack/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -p src/projectM-pulseaudio/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	qt -p /sbin/ldconfig
%postun	qt -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# COPYING is just license information, not actual LGPL text
%doc AUTHORS.txt FAQ.txt TODO.txt src/README src/libprojectM/{COPYING,ChangeLog}
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

%files qt
%defattr(644,root,root,755)
%doc src/projectM-qt/ReadMe
%attr(755,root,root) %{_libdir}/libprojectM-qt.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libprojectM-qt.so.1
%{_pixmapsdir}/prjm16-transparent.svg

%files qt-devel
%defattr(644,root,root,755)
%doc src/projectM-qt/ReadMe
%attr(755,root,root) %{_libdir}/libprojectM-qt.so
%{_includedir}/%{name}-qt
%{_pkgconfigdir}/libprojectM-qt.pc

%if %{with jack}
%files -n jack-projectM
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/projectM-jack
%{_desktopdir}/projectM-jack.desktop
%{_mandir}/man1/projectM-jack.1*
%endif

%files -n pulseaudio-projectM
%defattr(644,root,root,755)
%doc src/projectM-pulseaudio/AUTHORS
%attr(755,root,root) %{_bindir}/projectM-pulseaudio
%{_desktopdir}/projectM-pulseaudio.desktop
%{_mandir}/man1/projectM-pulseaudio.1*

%files -n libvisual-projectM
%defattr(644,root,root,755)
%doc src/projectM-libvisual/{ChangeLog,AUTHORS}
%attr(755,root,root) %{_bindir}/projectM-libvisual-alsa
%attr(755,root,root) %{_libdir}/libvisual-0.4/actor/libprojectM_libvisual.so
%{_desktopdir}/projectM-libvisual-alsa.desktop
