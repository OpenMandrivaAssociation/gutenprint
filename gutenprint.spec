%define _disable_ld_no_undefined 1
%define debug 0

%define drvver	5.2
%define major	2
%define libname %mklibname gutenprint %{major}
%define devname %mklibname gutenprint -d

%define uiapi	2
%define uimajor	1
%define libnameui %mklibname gutenprintui %{uiapi} %{uimajor}
%define devnameui %mklibname gutenprintui -d

%define corposerver %(perl -e 'print ("%{release}" =~ /mlcs/ ? 1 : 0)')
%define cups_serverbin %{_exec_prefix}/lib/cups

%if %{corposerver}
%define gimpplugin 0
%else
%define gimpplugin 1
%endif

Summary:	Photo-quality printer drivers primarily for inkjet printers
Name:		gutenprint
Version:	5.2.9
Release:	7
License:	GPLv2+
Group:		Publishing
Url:		http://gimp-print.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/gimp-print/%{name}-%{drvver}/%{version}/%{name}-%{version}.tar.bz2
Patch1:		gutenprint-5.0.1-menu.patch
Patch2:		gutenprint-5.2.7-fix-brother-hl-2030-support.patch
Patch3:		gutenprint-5.2.3-default-a4.patch

BuildRequires:	bison
BuildRequires:	chrpath
BuildRequires:	flex
BuildRequires:	foomatic-db
BuildRequires:	foomatic-db-engine
BuildRequires:	cups-devel >= 1.2.0
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(ijs)
BuildRequires:	pkgconfig(libtiff-4)
%if %{gimpplugin}
BuildRequires:	pkgconfig(gimp-2.0)
%endif

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

%package -n %{libname}
Summary:	Shared library for high-quality image printing
Group:		Publishing

%description -n %{libname}
This is a high-quality printing library used by the Gutenprint plugin,
the Gutenprint IJS color/photo inkjet/laser driver for GhostScript,
and by specialized CUPS drivers.

%package -n %{devname}
Summary:	Headers and links for compiling against libname
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}gutenprint2-devel < 5.2.9-3

%description -n %{devname}
These are the links and header files to compile applications which
should use the libname library.

%package -n %{libnameui}
Summary:	Shared library for Gutenprint GUI with GTK 2.x
Group:		Publishing

%description -n %{libnameui}
This is a GTK-2.x-based GUI library to create dialogs to control
the Gutenprint printer drivers.

%package -n %{devnameui}
Summary:	Headers and links for compiling against libnameui
Group:		Development/C
Requires:	%{libnameui} >= %{version}-%{release}
Provides:	%{name}ui-devel = %{version}-%{release}
Obsoletes:	%{_lib}gutenprintui2_1-devel < 5.2.9-3

%description -n %{devnameui}
These are the links and header files to compile applications which
should use the libnameui library.

%package common
Summary:	Documentation, samples and translations of Gutenprint
Provides:	gimpprint-common
Group:		Publishing

%description common
Documentation, sample files, and translations of Gutenprint.

%package cups
Summary:	Special CUPS printer driver of Gutenprint
Group:		Publishing
Requires:	cups >= 1.1
Requires:	gutenprint-common >= %{version}-%{release}

%description cups
This package contains a special Gutenprint printer driver to be used
with CUPS (and without GhostScript) and also the appropriate PPD files
to set up print queues with this driver.

With the Gutenprint CUPS drivers you can do a colour caibration. Use
the program "cups-calibrate" to perform it.

%package ijs
Summary:	Gutenprint IJS plugin for GhostScript
Group:		Publishing
Requires:	ghostscript >= 7.05
Requires:	gutenprint-common >= %{version}-%{release}

%description ijs
This package contains a Gutenprint plugin for GhostScripts IJS
interface. This gives access to the high printing quality of
Gutenprint with every GhostScript version containing the IJS
interface. Install also the gutenprint-foomatic package for easy setup
of print queues with arbitrary printing systems.

%package foomatic
Summary:	Foomatic data for Gutenprint IJS plugin for GhostScript
Group:		Publishing
Requires:	foomatic-db
Requires:	foomatic-db-engine

%description foomatic
Foomatic data for the Gutenprint IJS plug-in for GhostScript. You need
this package to set up print queues with printerdrake, KDE Printing
Manager, or directly with Foomatic.

%package escputil
Summary:	Gutenprint ink level monitor and printer maintenance tool
Group:		Publishing
Requires:	gutenprint-common >= %{version}-%{release}

%description escputil
This is a command line tool to query ink levels and to maintain
Epson's inkjet printers. It allows ink level query, head alignment,
nozzle checking, and nozzle cleaning. If you want a graphical
interface, use mtink instead.

%if %{gimpplugin}
%package gimp2
Summary:	Gutenprint plugin for high-quality image printing
Group:		Publishing
Requires:	gimp
Requires:	gutenprint-common >= %{version}-%{release}
%endif

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
%setup -q
%apply_patches

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
%define enablegimpplugin --with-gimp2
%else
%define enablegimpplugin --without-gimp2
%endif

%configure2_5x \
	--disable-static \
	--enable-shared \
	--enable-libgutenprintui2 \
	%enablegimpplugin \
	--with-cups \
	--enable-cups-level3-ppds \
	--enable-simplified-cups-ppds \
	--disable-static-genppd \
	--disable-translated-cups-ppds \
	--with-foomatic \
	--with-foomatic3 \
	%enabledebug

# Compile Gutenprint
%make


%install
# Change compiler flags for debugging when in debug mode
%if %debug
export DONT_STRIP=1
export CFLAGS="`echo %optflags |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/'`"
export CXXFLAGS="`echo %optflags |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/'`"
export RPM_OPT_FLAGS="`echo %optflags |sed -e 's/-O3/-g/' |sed -e 's/-O2/-g/'`"
%endif

%makeinstall_std

# Remove /usr/share/foomatic/kitload.log
rm -f %{buildroot}%{_datadir}/foomatic/kitload.log

# Remove "canon" and "epson" CUPS backends
rm -f %{buildroot}%{_prefix}/lib*/cups/backend/canon
rm -f %{buildroot}%{_prefix}/lib*/cups/backend/epson

# Remove a GTK-1.x file which is installed even when GTK-1.x support
# is disabled (Gutenprint bug)
rm -f %{buildroot}%{_libdir}/pkgconfig/gutenprintui.pc

# Fix up rpath.
for file in \
  %{buildroot}%{_sbindir}/cups-genppd.5.2 \
  %{buildroot}%{_libdir}/gimp/*/plug-ins/* \
  %{buildroot}%{_libdir}/*.so.* \
  %{buildroot}%{cups_serverbin}/driver/* \
  %{buildroot}%{cups_serverbin}/filter/* \
  %{buildroot}%{_bindir}/*
do
  chrpath --delete ${file}
done

# Translation files of Gutenprint
rm -f %{buildroot}/%{_datadir}/locale/*/*.po
%find_lang %{name}

%post cups
# Restart the CUPS daemon when it is running, but do not start it when it
# is not running. The restart of the CUPS daemon updates the CUPS-internal
# PPD index
/sbin/service cups condrestart || :
# Update print queues with Gutenprint CUPS driver
/usr/sbin/cups-genppdupdate > /dev/null 2>/dev/null || :

%post foomatic
# Update print queues with Gimp-Print/Gutenprint IJS driver
ls /etc/cups/ppd/*.ppd > /dev/null 2>&1 && \
for f in /etc/cups/ppd/*.ppd; do \
	queue=`basename ${f%%.ppd}`; \
	egrep -q '\*FoomaticIDs.*(gimp-print|gutenprint)' $f && \
		foomatic-configure -n $queue -f \
			-d gutenprint-ijs.%{drvver} \
			>/dev/null 2>&1 || :; \
done
exit 0

%postun cups
# Restart the CUPS daemon when it is running, but do not start it when it
# is not running. The restart of the CUPS daemon updates the CUPS-internal
# PPD index
# Do not restart on upgrades, as it is already restarted by post section.
if [ $1 -eq 1 ]; then
	/sbin/service cups condrestart || :
fi

%files -n %{libname}
%{_libdir}/libgutenprint.so.%{major}*
%dir %{_libdir}/gutenprint/*

%files -n %{devname}
%{_libdir}/libgutenprint.so
%{_libdir}/pkgconfig/gutenprint.pc
%{_includedir}/gutenprint

%files -n %{libnameui}
%{_libdir}/libgutenprintui%{uiapi}.so.%{uimajor}*

%files -n %{devnameui}
%{_libdir}/libgutenprintui2.so
%{_libdir}/pkgconfig/gutenprintui2.pc
%{_includedir}/gutenprintui2

%files common -f %{name}.lang
%doc ABOUT-NLS AUTHORS NEWS README
%{_bindir}/testpattern
%{_datadir}/gutenprint
%dir %{_libdir}/gutenprint
%dir %{_libdir}/gutenprint/%{drvver}
%dir %{_libdir}/gutenprint/%{drvver}/modules
%{_libdir}/gutenprint/%{drvver}/modules/*.so

%files cups
%config(noreplace) %{_sysconfdir}/cups/command.*
%{_bindir}/cups-*
%{_sbindir}/cups-*
%{_datadir}/cups/calibrate.ppm
%{cups_serverbin}/driver/gutenprint.%{drvver}
%{cups_serverbin}/filter/*
%{_mandir}/man8/cups-*

%files ijs
%{_bindir}/ijsgutenprint*
%{_mandir}/man1/ijsgutenprint.1*

%files foomatic
%{_datadir}/foomatic/db/*/*/*.xml

%files escputil
%attr(0755,lp,sys) %{_bindir}/escputil
%{_mandir}/man1/escputil*

%if %{gimpplugin}
%files gimp2
%{_libdir}/gimp/2.0/plug-ins/gutenprint
%endif

