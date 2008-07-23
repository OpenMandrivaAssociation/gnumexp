%define numexp_version 0.11.0
%define orbit_version 2.12.1
%define pymathml_version 0.3-2mdk

Summary:	GUI frontend for NumExp-core
Name:		gnumexp
Version:	0.11.0
Release:	%mkrel 3
License:	GPL
Group:		Sciences/Mathematics
URL:		http://numexp.sourceforge.net/
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
BuildRequires:	gnome-doc-utils
BuildRequires:	python-pygoocanvas
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils

Requires(post): GConf2
Requires(preun): GConf2
Requires(post): shared-mime-info
Requires(postun): shared-mime-info
Requires:	urw-fonts
Requires:	numexp-core >= %{numexp_version}
Requires:	ORBit2 >= %{orbit_version}
Requires:	docbook-dtd-mathml20
%if %mdkversion < 200710
Requires: pymathml >= %{pymathml_version}
%else
Requires: python-pymathml >= %{pymathml_verison}
%endif
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
%configure2_5x --disable-schemas-install

%make

%install
rm -rf %{buildroot}
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall DISABLE_MIME_INSTALL=1

#icons
mkdir -p %{buildroot}%{_miconsdir} \
	 %{buildroot}%{_iconsdir} \

install -m 0644 -D      data/gnumexp_icon.png %{buildroot}%{_liconsdir}/%{name}.png
convert -geometry 32x32 data/gnumexp_icon.png %{buildroot}%{_iconsdir}/%{name}.png
convert -geometry 16x16 data/gnumexp_icon.png %{buildroot}%{_miconsdir}/%{name}.png

desktop-file-install --vendor='' \
	--dir %{buildroot}%{_datadir}/applications/ \
	--remove-category="Application" \
	--add-category="Education" \
	--add-category="Science" \
	--add-category="Math" \
	%{buildroot}%{_datadir}/applications/*.desktop

%{find_lang} %{name}

# remove files not bundled
rm -f	%{buildroot}%{_libdir}/orbit-2.0/*.{a,la} \
	%{buildroot}%{_libdir}/python?.?/site-packages/*.{a,la}

%if %mdkversion < 200900
%post
%update_menus
%post_install_gconf_schemas numexp-console
%update_mime_database
%endif

%preun
%preun_uninstall_gconf_schemas numexp-console

%if %mdkversion < 200900
%postun
%clean_menus
%clean_mime_database
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}
%{_libdir}/%{name}
%{_datadir}/mime/packages/*.xml
%{_datadir}/pixmaps/*
%{_datadir}/pixmaps/%{name}
%{_datadir}/gnome/help/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_sysconfdir}/gconf/schemas/*.schemas
