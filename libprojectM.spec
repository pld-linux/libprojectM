%define		pkgname	projectM
Summary:	Awesome music visualizer
Summary(pl.UTF-8):	Imponujący wizualizator muzyki
Name:		libprojectM
Version:	2.1.0
Release:	1
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
BuildRequires:	OpenGL-devel
BuildRequires:	QtCore-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtOpenGL-devel
BuildRequires:	QtXml-devel
BuildRequires:	SDL-devel
BuildRequires:	cmake >= 2.6.0
BuildRequires:	desktop-file-utils
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	ftgl-devel >= 2.1.3
BuildRequires:	glew-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	libgomp-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libvisual-devel = 0.4.0
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	rpmbuild(macros) >= 1.577
BuildRequires:	sed >= 4.0
Requires:	fonts-TTF-bitstream-vera
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
Summary:	The Qt frontend to the projectM visualization plugin
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description qt
projectM-qt is a GUI designed to enhance the projectM user and preset
writer experience. It provides a way to browse, search, rate presets
and setup preset playlists for jack-projectM and pulseaudio-projectM.

%package qt-devel
Summary:	Header files for projectM QT library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki projectM QT
Group:		Development/Libraries
Requires:	%{name}-qt = %{epoch}:%{version}-%{release}

%description qt-devel
Header files for projectM QT library.

%description qt-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki projectM QT.

%package -n jack-projectM
Summary:	The projectM visualization plugin for jack
License:	GPLv2+ and MIT
Group:		Applications/Multimedia

%description -n jack-projectM
This package allows the use of the projectM visualization plugin
through any JACK compatible applications.

%package -n pulseaudio-projectM
Summary:	The projectM visualization plugin for pulseaudio
Group:		Applications/Multimedia

%description -n pulseaudio-projectM
This package allows the use of the projectM visualization plugin
through any pulseaudio compatible applications.

%package -n libvisual-projectM
Summary:	ProjectM plugin for libvisual
Summary(pl.UTF-8):	Wtyczka ProjectM dla libvisual
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n libvisual-projectM
projectM is a reimplementation of Milkdrop under OpenGL. This is a
plugin for libvisual visualization library.

%description -n libvisual-projectM -l pl.UTF-8
projectM jest reimplementacją projektu Milkdrop na OpenGL. Ten pakiet
zawiera wtyczkę dla biblioteki wizualizacji libvisual.

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
	-DINCLUDE-PROJECTM-TEST=OFF \
	-DINCLUDE-PROJECTM-JACK=ON \
	-DINCLUDE-PROJECTM-LIBVISUAL-ALSA=ON \
	../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post qt -p /sbin/ldconfig
%postun qt -p /sbin/ldconfig

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

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libprojectM-qt.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libprojectM-qt.so.1
%{_pixmapsdir}/prjm16-transparent.svg

%files qt-devel
%defattr(644,root,root,755)
%doc src/projectM-qt/ReadMe
%{_includedir}/%{name}-qt
%{_libdir}/libprojectM-qt*.so
%{_pkgconfigdir}/libprojectM-qt.pc

%files -n jack-projectM
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/projectM-jack
%{_desktopdir}/projectM-jack.desktop

%files -n pulseaudio-projectM
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/projectM-pulseaudio
%{_desktopdir}/projectM-pulseaudio.desktop

%files -n libvisual-projectM
%defattr(644,root,root,755)
%doc src/projectM-libvisual/{ChangeLog,AUTHORS}
%attr(755,root,root) %{_bindir}/projectM-libvisual-alsa
%attr(755,root,root) %{_libdir}/libvisual-0.4/actor/libprojectM_libvisual.so
%{_desktopdir}/projectM-libvisual-alsa.desktop
