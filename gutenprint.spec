%define version 5.0.2
%define driverversion 5.0
%define extraversion %nil
#define extraversion -rc3
%define release %mkrel 4
%define gutenprintmajor 2
%define libgutenprint %mklibname gutenprint %{gutenprintmajor}
%define gutenprintui2major 1
%define libgutenprintui2 %mklibname gutenprintui2_ %{gutenprintui2major}

%define corposerver %(perl -e 'print ("%release" =~ /mlcs/ ? 1 : 0)')

%if %{corposerver}
%define gimpplugin 0
%else
%define gimpplugin 1
%endif

%define debug 0

##### RPM PROBLEM WORKAROUNDS

# Suppress automatically generated Requires for Perl libraries.
#define _requires_exceptions perl\(.*\)

#define _unpackaged_files_terminate_build       0 
#define _missing_doc_files_terminate_build      0


Summary: Photo-quality printer drivers primarily for inkjet printers
Name:		gutenprint
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		Publishing
URL:		http://gimp-print.sourceforge.net/

##### GENERAL BUILDREQUIRES

BuildRequires:	autoconf2.5
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	foomatic-db
BuildRequires:	foomatic-db-engine
#BuildRequires:	glib-devel
BuildRequires:	libcups-devel >= 1.2.0-0.5361.0mdk
BuildRequires:	libgtk+2-devel
BuildRequires:	libijs-devel
BuildRequires:	libjpeg-static-devel
BuildRequires:	libtiff-devel

%if %{gimpplugin}
BuildRequires:	libgimp-devel
%endif

# Only needed when building Gutenprint from a CVS snapshot
#BuildRequires: tetex-latex ImageMagick docbook-utils sgml-tools

##### GIMP PRINT SOURCE
Source:	http://cesnet.dl.sourceforge.net/sourceforge/gimp-print/gutenprint-%{version}%{extraversion}.tar.bz2

##### GIMP PRINT PATCHES
Patch0:		gutenprint-5.0.1-noO6.patch
Patch1:		gutenprint-5.0.1-menu.patch
Patch3:		gutenprint-5.0.1-default-a4.patch
# https://qa.mandriva.com/show_bug.cgi?id=25453
Patch5:		gutenprint-5.0.2-locale.patch

##### BUILD ROOT
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

##### PACKAGE DESCRIPTIONS

%package -n %{libgutenprint}
Summary:	Shared library for high-quality image printing
Group:		Publishing
Provides:       libgutenprint = %{version}-%{release}

%package -n %{libgutenprint}-devel
Summary:	Headers and links for compiling against libgutenprint
Group:		Development/C
Requires:	%{libgutenprint} >= %{version}-%{release}
Requires:       multiarch-utils
Provides:       libgutenprint-devel = %{version}-%{release}
Provides:       gutenprint-devel = %{version}-%{release}

%package -n %{libgutenprintui2}
Summary:	Shared library for Gutenprint GUI with GTK 2.x
Group:		Publishing
Provides:       libgutenprintui2 = %{version}-%{release}

%package -n %{libgutenprintui2}-devel
Summary:	Headers and links for compiling against libgutenprintui2
Group:		Development/C
Requires:	%{libgutenprintui2} >= %{version}-%{release}
Requires:       multiarch-utils
Provides:       libgutenprintui2-devel = %{version}-%{release}

%package common
Summary: Documentation, samples and translations of Gutenprint
Obsoletes:	gimpprint-common
Provides:	gimpprint-common
Group: 		Publishing

%package cups
Summary: Special CUPS printer driver of Gutenprint
Requires: 	cups >= 1.1
Requires:	gutenprint-common >= %{version}-%{release}
Conflicts:	cups-drivers <= 10.1
%ifarch x86_64
Conflicts:	cups < 1.2.0-0.5361.0mdk
%endif
Obsoletes:	gimpprint-cups
Provides:	gimpprint-cups
Group: 		Publishing

%package ijs
Summary: Gutenprint IJS plugin for GhostScript
Requires:	ghostscript >= 7.05
Requires:	gutenprint-common >= %{version}-%{release}
Conflicts:	printer-filters <= 10.1
Obsoletes:	gimpprint-ijs
Provides:	gimpprint-ijs
Group:		Publishing

%package foomatic
Summary: Foomatic data for Gutenprint IJS plugin for GhostScript
Requires:	foomatic-db, foomatic-db-engine
Obsoletes:	gimpprint-foomatic
Provides:	gimpprint-foomatic
Group:		Publishing

%package escputil
Summary: Gutenprint ink level monitor and printer maintenance tool
Requires:	gutenprint-common >= %{version}-%{release}
Conflicts:	printer-utils <= 10.1
Obsoletes:	gimpprint-escputil
Provides:	gimpprint-escputil
Group:		Publishing

%if %{gimpplugin}
%package gimp2
Summary:	Gutenprint plugin for high-quality image printing
Group:		Publishing
Requires:	gimp >= 2.2.7-2mdk
Requires:	gutenprint-common >= %{version}-%{release}
Conflicts:      gimp < 2.2.7-2mdk
Obsoletes:	gimpprint-gimp2
Provides:	gimpprint-gimp2
%endif

##### DESCRIPTION TEXTS

%description
Gutenprint is a high quality printer driver suite for photo-quality
printing on inkjet printers, especially Epson. There are also some
Canon, HP, and Lexmark inkjets (older models) and PCL bw laser
printers supported (PCL 5e and earlier). If your printer is supported
by Gutenprint and not an HP printer supported by HPIJS, this is the
best choice of a free software printer driver.

Keep in mind that the leader of this project is hobby photographer and
wanted to get his 6-ink Epson Stylus Photo EX working in its best
quality without necessity of proprietary software.

%description -n %{libgutenprint}
This is a high-quality printing library used by the Gutenprint plugin,
the Gutenprint IJS color/photo inkjet/laser driver for GhostScript,
and by specialized CUPS drivers.

%description -n %{libgutenprint}-devel
These are the links and header files to compile applications which
should use the libgutenprint library.

%description -n %{libgutenprintui2}
This is a GTK-2.x-based GUI library to create dialogs to control
the Gutenprint printer drivers.

%description -n %{libgutenprintui2}-devel
These are the links and header files to compile applications which
should use the libgutenprintui2 library.

%description common
Documentation, sample files, and translations of Gutenprint.

%description cups
This package contains a special Gutenprint printer driver to be used
with CUPS (and without GhostScript) and also the appropriate PPD files
to set up print queues with this driver.

With the Gutenprint CUPS drivers you can do a colour caibration. Use
the program "cups-calibrate" to perform it.

%description ijs
This package contains a Gutenprint plugin for GhostScripts IJS
interface. This gives access to the high printing quality of
Gutenprint with every GhostScript version containing the IJS
interface. Install also the gutenprint-foomatic package for easy setup
of print queues with arbitrary printing systems.

%description foomatic
Foomatic data for the Gutenprint IJS plug-in for GhostScript. You need
this package to set up print queues with printerdrake, KDE Printing
Manager, or directly with Foomatic.

%description escputil
This is a command line tool to query ink levels and to maintain
Epson's inkjet printers. It allows ink level query, head alignment,
nozzle checking, and nozzle cleaning. If you want a graphical
interface, use mtink instead.

%if %{gimpplugin}
%description gimp2
This is a plug-in for the GIMP, which allows printing of images and
photos in very high quality on many modern inkjet printers and also
some lasers. Especially on Epson Stylus printers the quality which one
gets under proprietary operating systems is reached, due to Epson
publishing the protocols of their printers, but other brands of
printers give very high qualities, too. It can also output PostScript
to be able to print out of the GIMP on any printer.
%endif


%prep
# unpack main sources
%setup -q -n gutenprint-%{version}%{extraversion}
%patch0 -p1 -b .noO6
%patch1 -p1 -b .menu
%patch3 -p1 -b .a4
%patch5 -p1 -b .locale

%build
# Change compiler flags for debugging when in debug mode
%if %debug
export DONT_STRIP=1
export CFLAGS="`echo %optflags |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/'`"
export CXXFLAGS="`echo %optflags |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/'`"
export RPM_OPT_FLAGS="`echo %optflags |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/'`"
%endif

# "autogen.sh" needed for the case when Gutenprint
# driver is from CVS (see its README) or if build system is patched.
#export NOCONFIGURE=1; ./autogen.sh

# Build with all pipes and whistles: GIMP, GhostScript, CUPS, IJS, Foomatic,
# but without translated PPD files (does not work)
# Use IJS library provided by this package

%if %debug
%define enabledebug --enable-debug
%else
%define enabledebug %nil
%endif

%if %{gimpplugin}
%define enablegimpplugin --without-gimp --with-gimp2
%else
%define enablegimpplugin --without-gimp --without-gimp2
%endif

%configure2_5x \
	--enable-shared \
	--disable-rpath \
	--disable-libgutenprintui \
	--enable-libgutenprintui2 \
	%enablegimpplugin \
	--with-cups \
	--enable-cups-level3-ppds \
	--enable-simplified-cups-ppds \
	--disable-static-genppd \
	--disable-translated-cups-ppds \
	--with-ijs \
	--with-foomatic \
	--with-foomatic3 \
	%enabledebug

# Compile Gutenprint
%make


%install
rm -rf %{buildroot}

# Change compiler flags for debugging when in debug mode
%if %debug
export DONT_STRIP=1
export CFLAGS="`echo %optflags |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/'`"
export CXXFLAGS="`echo %optflags |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/'`"
export RPM_OPT_FLAGS="`echo %optflags |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/'`"
%endif

make DESTDIR=%{buildroot} install

# Remove /usr/share/foomatic/kitload.log
rm -f %{buildroot}%{_datadir}/foomatic/kitload.log

# Remove "canon" and "epson" CUPS backends
rm -f %{buildroot}%{_prefix}/lib*/cups/backend/canon
rm -f %{buildroot}%{_prefix}/lib*/cups/backend/epson

# Remove a GTK-1.x file which is installed even when GTK-1.x support
# is disabled (Gutenprint bug)
rm -f %{buildroot}%{_libdir}/pkgconfig/gutenprintui.pc

# Correct permissions
chmod a-x %{buildroot}%{_libdir}/*.la

# Translation files of Gutenprint
%find_lang gutenprint

# Multiarch setup
#multiarch_binaries %buildroot%{_bindir}/gutenprint-config


##### FILES

%files -n %{libgutenprint}
%defattr(-,root,root)
%{_libdir}/libgutenprint.so.*
%dir %{_libdir}/gutenprint/*
#dir %{_libdir}/gutenprint/*/modules
#{_libdir}/gutenprint/*/modules/*.so

%files -n %{libgutenprint}-devel
%defattr(-,root,root)
%{_libdir}/libgutenprint.so
%{_libdir}/libgutenprint.la
%{_libdir}/libgutenprint.a
#{_libdir}/gutenprint/*/modules/*.so
#{_libdir}/gutenprint/*/modules/*.la
#{_libdir}/gutenprint/*/modules/*.a
%{_libdir}/pkgconfig/gutenprint.pc
%{_includedir}/gutenprint

%files -n %{libgutenprintui2}
%defattr(-,root,root)
%{_libdir}/libgutenprintui2.so.*

%files -n %{libgutenprintui2}-devel
%defattr(-,root,root)
%{_libdir}/libgutenprintui2.so
%{_libdir}/libgutenprintui2.la
%{_libdir}/libgutenprintui2.a
%{_libdir}/pkgconfig/gutenprintui2.pc
%{_includedir}/gutenprintui2

%files common -f gutenprint.lang
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS NEWS README
%{_bindir}/testpattern
%{_datadir}/gutenprint
%dir %{_libdir}/gutenprint

%files cups
%defattr(-,root,root)
%{_mandir}/man8/cups-*
%{_bindir}/cups-*
%{_sbindir}/cups-*
#%{_datadir}/cups/model/*
%{_datadir}/cups/calibrate.ppm
#attr(0755,root,root) %{_prefix}/lib*/cups/backend/*
%attr(0755,root,root) %{_prefix}/lib*/cups/driver/gutenprint.%{driverversion}
%attr(0755,root,root) %{_prefix}/lib*/cups/filter/*
%config(noreplace) %{_sysconfdir}/cups/command.*

%files ijs
%defattr(-,root,root)
%{_mandir}/man1/ijsgutenprint.1*
%{_bindir}/ijsgutenprint*

%files foomatic
%defattr(-,root,root)
%_datadir/foomatic/db/*/*/*.xml

%files escputil
%defattr(-,root,root)
%{_mandir}/man1/escputil*
%attr(0755,lp,sys) %{_bindir}/escputil

%if %{gimpplugin}
%files gimp2
%defattr(-,root,root)
%{_libdir}/gimp/2.0/plug-ins/gutenprint
%endif

%post -n %{libgutenprint} -p /sbin/ldconfig

%post -n %{libgutenprintui2} -p /sbin/ldconfig

%post common
%_install_info gutenprint
:

%post cups
# Restart the CUPS daemon when it is running, but do not start it when it
# is not running. The restart of the CUPS daemon updates the CUPS-internal
# PPD index
/sbin/service cups condrestart || :
# Update print queues with Gutenprint CUPS driver
/usr/sbin/cups-genppdupdate.%{driverversion} > /dev/null 2>/dev/null || :

%post foomatic
# Update print queues with Gimp-Print/Gutenprint IJS driver
ls /etc/cups/ppd/*.ppd > /dev/null 2>&1 && \
for f in /etc/cups/ppd/*.ppd; do \
	queue=`basename ${f%%.ppd}`; \
	egrep -q '\*FoomaticIDs.*(gimp-print|gutenprint)' $f && \
		foomatic-configure -n $queue -f \
			-d gutenprint-ijs.%{driverversion} \
			>/dev/null 2>&1 || :; \
done
exit 0

%postun -n %{libgutenprint} -p /sbin/ldconfig

%postun -n %{libgutenprintui2} -p /sbin/ldconfig

%postun common
%_remove_install_info gutenprint
:

%postun cups
# Restart the CUPS daemon when it is running, but do not start it when it
# is not running. The restart of the CUPS daemon updates the CUPS-internal
# PPD index
# Do not restart on upgrades, as it is already restarted by post section.
if [ $1 -eq 1 ]; then
	/sbin/service cups condrestart || :
fi

%clean
rm -rf %{buildroot}

