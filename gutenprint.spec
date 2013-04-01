%define version 5.2.9
%define driverversion 5.2
%define extraversion %nil
#define extraversion -rc3
%define release %mkrel 1
%define gutenprintmajor 2
%define libgutenprint %mklibname gutenprint %{gutenprintmajor}
%define gutenprintui2major 1
%define libgutenprintui2 %mklibname gutenprintui2_ %{gutenprintui2major}

%define corposerver %(perl -e 'print ("%release" =~ /mlcs/ ? 1 : 0)')

%define cups_serverbin %{_exec_prefix}/lib/cups

%if %{corposerver}
%define gimpplugin 0
%else
%define gimpplugin 1
%endif

%define debug 0

##### RPM PROBLEM WORKAROUNDS

# Suppress automatically generated Requires for Perl libraries.
#define _requires_exceptions perl\(.*\)

#define _unpackaged_files_terminate_build	0 
#define _missing_doc_files_terminate_build	0
%define _disable_ld_no_undefined 1

Summary:	Photo-quality printer drivers primarily for inkjet printers
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
BuildRequires:	cups-devel >= 1.2.0
BuildRequires:	gtk+2-devel
BuildRequires:	libijs-devel
BuildRequires:	jpeg-static-devel
BuildRequires:	libtiff-devel
BuildRequires:	chrpath

%if %{gimpplugin}
BuildRequires:	gimp-devel
%endif

# Only needed when building Gutenprint from a CVS snapshot
#BuildRequires: tetex-latex imagemagick docbook-utils sgml-tools

##### GIMP PRINT SOURCE
Source0:	http://downloads.sourceforge.net/project/gimp-print/%{name}-%{driverversion}/%{version}/%{name}-%{version}%{extraversion}.tar.bz2

##### GIMP PRINT PATCHES
Patch1:		gutenprint-5.0.1-menu.patch
Patch3:		gutenprint-5.2.3-default-a4.patch

##### BUILD ROOT
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

##### PACKAGE DESCRIPTIONS

%package -n %{libgutenprint}
Summary:	Shared library for high-quality image printing
Group:		Publishing
Provides:	libgutenprint = %{version}-%{release}

%package -n %{libgutenprint}-devel
Summary:	Headers and links for compiling against libgutenprint
Group:		Development/C
Requires:	%{libgutenprint} >= %{version}-%{release}
Requires:	multiarch-utils
Provides:	libgutenprint-devel = %{version}-%{release}
Provides:	gutenprint-devel = %{version}-%{release}

%package -n %{libgutenprintui2}
Summary:	Shared library for Gutenprint GUI with GTK 2.x
Group:		Publishing
Provides:	libgutenprintui2 = %{version}-%{release}

%package -n %{libgutenprintui2}-devel
Summary:	Headers and links for compiling against libgutenprintui2
Group:		Development/C
Requires:	%{libgutenprintui2} >= %{version}-%{release}
Requires:	multiarch-utils
Provides:	libgutenprintui2-devel = %{version}-%{release}

%package common
Summary: Documentation, samples and translations of Gutenprint
Obsoletes:	gimpprint-common
Provides:	gimpprint-common
Group:		Publishing

%package cups
Summary: Special CUPS printer driver of Gutenprint
Requires:	cups >= 1.1
Requires:	gutenprint-common >= %{version}-%{release}
Conflicts:	cups-drivers <= 10.1
%ifarch x86_64
Conflicts:	cups < 1.2.0-0.5361.0mdk
%endif
Obsoletes:	gimpprint-cups
Provides:	gimpprint-cups
Group:		Publishing

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
Conflicts:	gimp < 2.2.7-2mdk
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
%patch1 -p1 -b .menu
%patch3 -p1 -b .a4

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

rm -rf  %{buildroot}%{_libdir}/*.la

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
find %{buildroot} -regex ".*/gutenprint.*.[mp]o" | sed -e "s@^%{buildroot}@@" > gutenprint.lang

# Multiarch setup
#multiarch_binaries % buildroot % {_bindir}/gutenprint-config


##### FILES

%files -n %{libgutenprint}
%defattr(-,root,root)
%{_libdir}/libgutenprint.so.*
%dir %{_libdir}/gutenprint/*
#dir % {_libdir}/gutenprint/*/modules
#{_libdir}/gutenprint/*/modules/*.so

%files -n %{libgutenprint}-devel
%defattr(-,root,root)
%{_libdir}/libgutenprint.so
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
#% {_datadir}/cups/model/*
%{_datadir}/cups/calibrate.ppm
#attr(0755,root,root) % {_prefix}/lib*/cups/backend/*
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

%if %mdkversion < 200900
%post -n %{libgutenprint} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libgutenprintui2} -p /sbin/ldconfig
%endif

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
			-d gutenprint-ijs.%{driverversion} \
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

%clean
rm -rf %{buildroot}



%changelog
* Mon Jul 09 2012 Alexander Khrukin <akhrukin@mandriva.org> 5.2.9-1mdv2012.0
+ Revision: 808563
- version update 5.2.9

* Fri Jun 15 2012 Alexander Khrukin <akhrukin@mandriva.org> 5.2.8-1
+ Revision: 805848
- version update 5.2.8

* Mon Oct 24 2011 Alexander Barakin <abarakin@mandriva.org> 5.2.7-1
+ Revision: 705895
- upstream version update and rpmlint fixes

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 5.2.6-2
+ Revision: 664962
- mass rebuild

* Sun Nov 28 2010 Sandro Cazzaniga <kharec@mandriva.org> 5.2.6-1mdv2011.0
+ Revision: 602333
- update to new version 5.2.6

* Fri Feb 12 2010 Frederik Himpe <fhimpe@mandriva.org> 5.2.5-1mdv2010.1
+ Revision: 505053
- update to new version 5.2.5

* Sat Aug 01 2009 Frederik Himpe <fhimpe@mandriva.org> 5.2.4-1mdv2010.0
+ Revision: 407312
- Update to new version 5.2.4
- Remove patch integrated upstream

* Tue Dec 23 2008 Frederik Himpe <fhimpe@mandriva.org> 5.2.3-1mdv2009.1
+ Revision: 317984
- Update to new version 5.2.3
- Rediff patch to use A4 by default, remove margins work-around as
  instructed by upstream comment in papers.xml
- Update no -O6 CFLAG patch from Fedora
- Use chrpath to remove rpaths (from Fedora)
- Gutenprint now needs installation of some po files in addition
  to mo files.
- postinstall script: genppdupdate.5.1 renamed to genppdupdate

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Sun Nov 09 2008 Oden Eriksson <oeriksson@mandriva.com> 5.1.7-3mdv2009.1
+ Revision: 301533
- rebuilt against new libxcb

* Tue Jun 24 2008 Tiago Salem <salem@mandriva.com.br> 5.1.7-2mdv2009.0
+ Revision: 228552
- rebuild to fix lzma payload issue

* Wed Jun 18 2008 Tiago Salem <salem@mandriva.com.br> 5.1.7-1mdv2009.0
+ Revision: 225977
- version 5.1.7
- remove locale patch as it is already in upstream source code.

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Jan 30 2008 Marcelo Ricardo Leitner <mrl@mandriva.com> 5.0.2-4mdv2008.1
+ Revision: 160235
- Remove patch optmize, as it may introduce problems with unstable networks.
- Use the same patch for locale as upstream used.
- Do not run autoconf on %%prep, it's not needed.

* Tue Jan 29 2008 Marcelo Ricardo Leitner <mrl@mandriva.com> 5.0.2-3mdv2008.1
+ Revision: 159908
- Rewrite lpstat patch in a better way. Closes: #25453

* Wed Jan 23 2008 Funda Wang <fwang@mandriva.org> 5.0.2-2mdv2008.1
+ Revision: 156979
- rebuild

* Tue Jan 08 2008 Marcelo Ricardo Leitner <mrl@mandriva.com> 5.0.2-1mdv2008.1
+ Revision: 146776
- New upstream: 5.0.2

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Nov 28 2007 Giuseppe Ghibò <ghibo@mandriva.com> 5.0.1-5mdv2008.1
+ Revision: 113646
- Disable -O6 compilation flag (Patch0).
- Let "Print with GutenPrint..." entry in GIMP "File" menu appear at a nicer place (Patch1).
- Default to A4 paper (Patch3).

* Thu Sep 13 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 5.0.1-4mdv2008.0
+ Revision: 85217
- gutenprint-foomatic should not require any driver, as it is just a database package.

* Thu Sep 13 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 5.0.1-3mdv2008.0
+ Revision: 85033
- Remove too-old conflict pointed by pixel.

* Tue Sep 04 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 5.0.1-2mdv2008.0
+ Revision: 79404
- Rebuilt against new ghostscript.

* Mon Jun 18 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 5.0.1-1mdv2008.0
+ Revision: 41029
- New stable upstream: 5.0.1

* Wed May 16 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 5.0.0.99.1-3mdv2008.0
+ Revision: 27398
- Do not restart the service while removing the old package during an upgrade,
  as it is already restart by the post section of the new one.
- New upstream: 5.0.0.99.1, with full support for CUPS 1.2
- Major specfile cleanup
- Do not redirect cups condrestart, as the user must be able to know
  that it is being restarted and if it failed to start.
- Special note: upstream now defaults to not generate ppd files when using CUPS
  1.2.

