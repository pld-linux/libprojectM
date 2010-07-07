%define		pkgname	projectM
Summary:	Awesome music visualizer
Summary(pl.UTF-8):	Imponujący wizualizator muzyki
Name:		libprojectM
Version:	2.0.1
Release:	1
Epoch:		1
License:	LGPL
Group:		Libraries
Source0:	http://downloads.sourceforge.net/project/projectm/%{version}/projectM-%{version}-Source.tar.gz
# Source0-md5:	f8bf795878cdbbef54784cf2390b4c89
Patch0:		%{name}-soname.patch
Patch1:		%{name}-fonts.patch
Patch2:		%{name}-static.patch
URL:		http://projectm.sourceforge.net/
BuildRequires:	cmake
BuildRequires:	ftgl-devel >= 2.1.3
BuildRequires:	glew-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.566
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

%build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DBUILD_PROJECTM_STATIC=yes \
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
