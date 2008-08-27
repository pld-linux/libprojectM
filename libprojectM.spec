#
%define		_name	projectM
#
Summary:	Awesome music visualizer
Summary(pl.UTF-8):	Imponujący wizualizator muzyki
Name:		libprojectM
Version:	1.1
Release:	3
Epoch:		1
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/projectm/%{name}-%{version}.tar.bz2
# Source0-md5:	3d939a4228f5e782620670961ac89aaf
Patch0:		%{name}-static.patch
URL:		http://projectm.sourceforge.net/
BuildRequires:	cmake
BuildRequires:	ftgl-devel >= 2.1.2-3
BuildRequires:	glew-devel
BuildRequires:	pkgconfig
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
%setup -q
%patch0 -p1
#workaround for library path
%{__sed} -i \
    -e 's#DESTINATION lib#DESTINATION %{_libdir}#' \
    CMakeLists.txt

%build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64 \
%endif
	.
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_libdir}/libprojectM.so.*.*
%ghost %attr(755,root,root) %{_libdir}/libprojectM.so.?
%dir %{_datadir}/%{_name}
%{_datadir}/%{_name}/config.inp
%dir %{_datadir}/%{_name}/fonts
%{_datadir}/%{_name}/fonts/*.ttf
%dir %{_datadir}/%{_name}/presets
%{_datadir}/%{_name}/presets/*.milk
%{_datadir}/%{_name}/presets/*.prjm
%{_datadir}/%{_name}/presets/*.tga

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libprojectM.so
%{_includedir}/%{name}
%{_pkgconfigdir}/libprojectM.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libprojectM.a
