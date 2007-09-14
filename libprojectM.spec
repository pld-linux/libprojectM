# TODO:
# - pl summary
#
%define		_name	projectM
Summary:	Awesome music visualizer
Summary(pl.UTF-8):	Imponujący wizualizator muzyki
Name:		lib%{_name}
Version:	0.99
Release:	0.1
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/xmms-projectm/%{name}-%{version}.tar.bz2
# Source0-md5:	20dc0aa2af96340c3209c9795cc3217d
URL:		http://xmms-projectm.sourceforge.net/
BuildRequires:	ftgl-devel >= 2.1.2-3
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
%setup -q -n %{name}

%build
%configure
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
%attr(755,root,root) %{_libdir}/libprojectM.so.*.*.*
%dir %{_datadir}/%{_name}
%{_datadir}/%{_name}/config
%{_datadir}/%{_name}/config.fastcomputers
%{_datadir}/%{_name}/config.slowcomputers
%dir %{_datadir}/%{_name}/fonts
%{_datadir}/%{_name}/fonts/*.ttf
%dir %{_datadir}/%{_name}/presets
%{_datadir}/%{_name}/presets/*.milk


%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libprojectM.so
%{_libdir}/libprojectM.la
%{_includedir}/%{_name}
%{_pkgconfigdir}/libprojectM.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libprojectM.a
