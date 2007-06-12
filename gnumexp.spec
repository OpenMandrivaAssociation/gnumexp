%define numexp_version 0.11.0
%define orbit_version 2.12.1
%define pymathml_version 0.3-2mdk

Summary:	GUI frontend for NumExp-core
Name:		gnumexp
Version:	0.10.0
Release:	%mkrel 6
License:	GPL
Group:		Sciences/Mathematics
URL:		http://numexp.sf.net/
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot
Source:		ftp://download.sourceforge.net/pub/sourceforge/numexp/%{name}-%{version}.tar.bz2

BuildRequires:	libnumexp-devel >= %{numexp_version}
BuildRequires:	numexp-core >= %{numexp_version}
BuildRequires:	libORBit2-devel >= %{orbit_version}
BuildRequires:  libbonoboui
BuildRequires:	libxml2-utils
BuildRequires:	gnome-python-extras >= 2.9.4
BuildRequires:	pygtk2.0-devel >= 2.5.3
BuildRequires:	pyorbit-devel >= 2.0.1
BuildRequires:	python-pymathml >= %{pymathml_version}
BuildRequires:	docbook-dtd-mathml20
BuildRequires:	libnxplot-python
BuildRequires:	libnxplot-devel
BuildRequires:	X11-Xvfb
BuildRequires:	perl-XML-Parser
# finding this one out is very painstaking
BuildRequires:	gnome-python-gnomeprint

Requires(post): GConf2
Requires(preun): GConf2
Requires(post): shared-mime-info
Requires(postun): shared-mime-info
Requires:	urw-fonts
Requires:	numexp-core >= %{numexp_version}
Requires:	ORBit2 >= %{orbit_version}
Requires:	pymathml >= %{pymathml_version}
Requires:	docbook-dtd-mathml20
Requires: pymathml
# prevent "Fatal Python error: can't initialise module _nxplot" error:
Requires: gnome-python-gnomeprint

%description
gNumExp is a GUI frontend to numexp-core. gNumExp can be considered
as a Mathematica-like mathematical application.

numexp-core is part of the NumExp project, which could be described as a
mathematical computation environment or even as a programming language.

%prep
%setup -q

%build
# (Abel) X display AND fontpath are necessary for pygtk detection
# :500 should be reasonable enough to avoid collision
# I want to f*ck mandrake building clusters
Xvfb -fp %{_datadir}/fonts/default/ghostscript -fp %{_prefix}/X11R6/%{_lib}/X11/fonts/misc :500 -nolisten unix & pid=$!
export DISPLAY=:500

%configure2_5x --disable-schemas-install || \
	{ kill $pid; exit 1; }

kill $pid

%make

%install
rm -rf %{buildroot}
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std DISABLE_MIME_INSTALL=1

#icons
mkdir -p %{buildroot}%{_miconsdir} \
	 %{buildroot}%{_iconsdir} \

install -m 0644 -D      pixmaps/gnumexp_icon.png %{buildroot}%{_liconsdir}/%{name}.png
convert -geometry 32x32 pixmaps/gnumexp_icon.png %{buildroot}%{_iconsdir}/%{name}.png
convert -geometry 16x16 pixmaps/gnumexp_icon.png %{buildroot}%{_miconsdir}/%{name}.png

%{find_lang} %{name}

# remove files not bundled
rm -f	%{buildroot}%{_libdir}/orbit-2.0/*.{a,la} \
	%{buildroot}%{_libdir}/python?.?/site-packages/*.{a,la}

%post
%update_menus
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
for SCHEMA in numexp-console; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$SCHEMA.schemas > /dev/null
done
%{_bindir}/update-mime-database %{_datadir}/mime > /dev/null

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  for SCHEMA in numexp-console; do
    gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/$SCHEMA.schemas > /dev/null
  done
fi

%postun
%clean_menus
%{_bindir}/update-mime-database %{_datadir}/mime > /dev/null

%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%doc README
%{_bindir}/*
%{_datadir}/application-registry/*.applications
%{_datadir}/applications/*.desktop
%{_datadir}/gnome-2.0/ui/*.xml
%{_datadir}/%{name}
%{_datadir}/idl/*.idl
%{_datadir}/mime-info/%{name}.*
%{_datadir}/mime/packages/*.xml
%{_datadir}/pixmaps/*
%{_libdir}/bonobo/servers/*.server
%{_libdir}/orbit-2.0/*.so
%{_libdir}/python?.?/site-packages/*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_sysconfdir}/gconf/schemas/*.schemas

