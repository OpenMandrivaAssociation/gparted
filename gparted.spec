%define _files_listed_twice_terminate_build 0

Summary:	Graphical frontend to libparted
Name:		gparted
Version:	1.3.0
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		https://gparted.org/
Source0:	https://sourceforge.net/projects/%{name}/files/%{name}/%{name}-%{version}/%{name}-%{version}.tar.gz
#Source2:	gparted-console.apps
#Source3:	gparted-pam.d

BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:	intltool
BuildRequires:	rarian
BuildRequires:	yelp-tools
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gtkmm-3.0)
BuildRequires:	pkgconfig(libparted)
BuildRequires:	pkgconfig(sigc++-2.0)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	polkit
Requires:	polkit
Requires:	usermode-consoleonly
Recommends:	dosfstools
Recommends:	mtools

%description
GParted stands for Gnome Partition Editor and is a graphical frontend to 
libparted. Among other features it supports creating, resizing, moving 
and copying of partitions.

%prep
%autosetup -p1

%build
%configure --enable-libparted-dmraid
%make_build

%install
%make_install
%find_lang %{name} --with-gnome

#consolehelper
#mkdir -p %{buildroot}%{_bindir}
#ln -s consolehelper %{buildroot}%{_bindir}/gparted
#sed -i 's|%{_sbindir}|%{_bindir}|' %{buildroot}%{_datadir}/applications/*.desktop

#mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
#cp %{SOURCE2} %{buildroot}%{_sysconfdir}/security/console.apps/gparted

#mkdir -p %{buildroot}%{_sysconfdir}/pam.d
#cp %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/gparted

desktop-file-install --vendor='' \
	--dir %{buildroot}%{_datadir}/applications/ \
	--remove-category=GNOME \
	--add-category='GTK;HardwareSettings;Settings' \
	%{buildroot}%{_datadir}/applications/*.desktop

%files -f %{name}.lang
%doc AUTHORS README COPYING ChangeLog
#config(noreplace) %{_sysconfdir}/pam.d/gparted
#config(noreplace) %{_sysconfdir}/security/console.apps/gparted
%{_bindir}/%{name}
%{_sbindir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/polkit-1/actions/org.gnome.gparted.policy
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man8/*
