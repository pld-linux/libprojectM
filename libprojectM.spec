# TODO:
# - pl summary
# - test if it works
#
%define		_name	projectM
Summary:	Awesome music visualizer
Summary(pl.UTF-8):	Imponujący wizualizator muzyki
Name:		libprojectM
Version:	1.0
Release:	0.1
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/sourceforge/projectm/%{name}-%{version}.tar.bz2
# Source0-md5:	66d2405fcb03efd4c82a0ea1989b4cbc
Patch0:		%{name}-static.patch
URL:		http://projectm.sourceforge.net/
BuildRequires:	cmake
BuildRequires:	glew-devel
BuildRequires:	ftgl-devel >= 2.1.2-3
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
projectM is a reimplementation of Milkdrop under OpenGL. It is an
awesome music visualizer. There is nothing better in the world of
Unix.

%package devel
Summary:	Header files for projectM library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki projectM
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for projectM library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki projectM.

%package static
Summary:	Static projectM library
Summary(pl.UTF-8):	Statyczna biblioteka projectM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

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
    -e 's#lib/pkgconfig#%{_lib}/pkgconfig#' \
    CMakeLists.txt

%build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
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
%attr(755,root,root) %{_libdir}/libprojectM.so
%dir %{_datadir}/%{_name}
%{_datadir}/%{_name}/config.inp
%dir %{_datadir}/%{_name}/fonts
%{_datadir}/%{_name}/fonts/*.ttf
%dir %{_datadir}/%{_name}/presets
%{_datadir}/%{_name}/presets/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
%{_pkgconfigdir}/libprojectM.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libprojectM.a
