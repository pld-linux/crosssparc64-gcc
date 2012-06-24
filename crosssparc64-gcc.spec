Summary:	Cross SPARC64 GNU binary utility development utilities - gcc
Summary(es):	Utilitarios para desarrollo de binarios de la GNU - SPARC64 gcc
Summary(fr):	Utilitaires de d�veloppement binaire de GNU - SPARC64 gcc
Summary(pl):	Skro�ne narz�dzia programistyczne GNU dla SPARC64 - gcc
Summary(pt_BR):	Utilit�rios para desenvolvimento de bin�rios da GNU - SPARC64 gcc
Summary(tr):	GNU geli�tirme ara�lar� - SPARC64 gcc
Name:		crosssparc64-gcc
Version:	3.4.3
Release:	1
Epoch:		1
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	e744b30c834360fccac41eb7269a3011
Patch0:		%{name}-pr17601.patch
BuildRequires:	crosssparc64-binutils
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	automake
BuildRequires:	/bin/bash
Requires:	crosssparc64-binutils
Requires:	gcc-dirs
Obsoletes:	egcs64
ExcludeArch:	sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		sparc64-pld-linux
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_libdir}/gcc/%{target}
%define		gcclib		%{gccarch}/%{version}

%define		_noautostrip	.*%{gcclib}.*/libgc.*\\.a

%description
This package contains a cross-gcc which allows the creation of
binaries to be run on SPARC64 linux (architecture sparc64-linux)
on other machines.

%description -l de
Dieses Paket enth�lt einen Cross-gcc, der es erlaubt, auf einem
anderem Rechner Code f�r sparc64-Linux zu generieren.

%description -l pl
Ten pakiet zawiera skro�ny gcc pozwalaj�cy na robienie na innych
maszynach binari�w do uruchamiania na SPARC64 (architektura
"sparc64-linux").

%prep
%setup -q -n gcc-%{version}
%patch0 -p0

%build
cp -f /usr/share/automake/config.sub .
rm -rf obj-%{target}
install -d obj-%{target}
cd obj-%{target}

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
TEXCONFIG=false \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--disable-shared \
	--disable-threads \
	--enable-languages="c" \
	--enable-c99 \
	--enable-long-long \
	--with-gnu-as \
	--with-gnu-ld \
	--with-system-zlib \
	--with-multilib \
	--without-headers \
	--without-x \
	--target=%{target} \
	--host=%{_target_platform} \
	--build=%{_target_platform}

%{__make} all-gcc

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C obj-%{target} install-gcc \
	DESTDIR=$RPM_BUILD_ROOT

# don't want this here
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a

%if 0%{!?debug:1}
%{target}-strip -g $RPM_BUILD_ROOT%{gcclib}/32/libgcc.a
%{target}-strip -g $RPM_BUILD_ROOT%{gcclib}/32/libgcov.a
%{target}-strip -g $RPM_BUILD_ROOT%{gcclib}/libgcc.a
%{target}-strip -g $RPM_BUILD_ROOT%{gcclib}/libgcov.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-cpp
%attr(755,root,root) %{_bindir}/%{target}-gcc
%dir %{gccarch}
%dir %{gcclib}
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
%dir %{gcclib}/32
%{gcclib}/32/crt*.o
%{gcclib}/32/libgcc.a
%{gcclib}/crt*.o
%{gcclib}/libgcc.a
%{gcclib}/specs*
%dir %{gcclib}/include
%{gcclib}/include/*.h
%{_mandir}/man1/%{target}-cpp.1*
%{_mandir}/man1/%{target}-gcc.1*
