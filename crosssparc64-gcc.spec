#
# TODO:
#		- symlinks {lib64,ld-*}
#
Summary:	Cross SPARC64 GNU binary utility development utilities - gcc
Summary(es):	Utilitarios para desarrollo de binarios de la GNU - SPARC64 gcc
Summary(fr):	Utilitaires de développement binaire de GNU - SPARC64 gcc
Summary(pl):	Skro¶ne narzêdzia programistyczne GNU dla SPARC64 - gcc
Summary(pt_BR):	Utilitários para desenvolvimento de binários da GNU - SPARC64 gcc
Summary(tr):	GNU geliþtirme araçlarý - SPARC64 gcc
Name:		crosssparc64-gcc
Version:	3.4.2
Release:	2
Epoch:		1
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	2fada3a3effd2fd791df09df1f1534b3
Patch0:		%{name}-pr17601.patch
BuildRequires:	crosssparc64-binutils
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	automake
BuildRequires:	/bin/bash
Requires:	crosssparc64-binutils
ExcludeArch:	sparc64
Obsoletes:	egcs64
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
Dieses Paket enthält einen Cross-gcc, der es erlaubt, auf einem
anderem Rechner Code für sparc64-Linux zu generieren.

%description -l pl
Ten pakiet zawiera skro¶ny gcc pozwalaj±cy na robienie na innych
maszynach binariów do uruchamiania na SPARC64 (architektura
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
	--with-gnu-as \
	--with-gnu-ld \
	--with-system-zlib \
	--with-multilib \
	--with-newlib \
	--without-headers \
	--without-x \
	--target=%{target} \
	--host=%{_target_platform} \
	--build=%{_target_platform}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C obj-%{target} install \
	DESTDIR=$RPM_BUILD_ROOT

# don't want this here
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a

%{target}-strip -g $RPM_BUILD_ROOT%{gcclib}/libgcov.a
%if 0%{!?debug:1}
%{target}-strip -g $RPM_BUILD_ROOT%{gcclib}/libgcc.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-cpp
%attr(755,root,root) %{_bindir}/%{target}-gcc*
%attr(755,root,root) %{_bindir}/%{target}-gcov
%dir %{gccarch}
%dir %{gcclib}
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
%{gcclib}/crt*.o
%{gcclib}/libgcc.a
%{gcclib}/specs*
%dir %{gcclib}/32
%{gcclib}/32/crt*.o
%{gcclib}/32/libgcc.a
%dir %{gcclib}/include
%{gcclib}/include/*.h
%{_mandir}/man1/%{target}-gcc.1*
