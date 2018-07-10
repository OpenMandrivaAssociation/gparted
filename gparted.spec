%define _files_listed_twice_terminate_build 0

Summary:	Graphical frontend to libparted
Name:		gparted
Version:	0.22.0
Release:	3
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://gparted.sourceforge.net
Source0:	http://downloads.sourceforge.net/project/gparted/%{name}/%{name}-%{version}/%{name}-%{version}.tar.bz2
Source2:	gparted-console.apps
Source3:	gparted-pam.d

BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:	intltool
BuildRequires:	rarian
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gtkmm-2.4)
BuildRequires:	pkgconfig(libparted)
BuildRequires:	pkgconfig(sigc++-2.0)
BuildRequires:	pkgconfig(uuid)
Requires:		usermode-consoleonly

%description
GParted stands for Gnome Partition Editor and is a graphical frontend to 
libparted. Among other features it supports creating, resizing, moving 
and copying of partitions.

%prep
%setup -q

%build
%configure --enable-libparted-dmraid
%make

%install
%makeinstall_std
%find_lang %{name} --with-gnome

#consolehelper
mkdir -p %{buildroot}%{_bindir}
ln -s consolehelper %{buildroot}%{_bindir}/gparted
sed -i 's|%{_sbindir}|%{_bindir}|' %{buildroot}%{_datadir}/applications/*.desktop

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/security/console.apps/gparted

mkdir -p %{buildroot}%{_sysconfdir}/pam.d
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/gparted

desktop-file-install --vendor='' \
	--dir %{buildroot}%{_datadir}/applications/ \
	--remove-category=GNOME \
	--add-category='GTK;HardwareSettings;Settings' \
	%{buildroot}%{_datadir}/applications/*.desktop

%preun
if [ $1 -ge 0 ]; then
    if [ -a %{_datadir}/hal/fdi/policy/gparted-disable-automount.fdi ]; then
       rm -rf %{_datadir}/hal/fdi/policy/gparted-disable-automount.fdi
    fi
fi

%files -f %{name}.lang
%doc AUTHORS README COPYING ChangeLog
%config(noreplace) %{_sysconfdir}/pam.d/gparted
%config(noreplace) %{_sysconfdir}/security/console.apps/gparted
%{_bindir}/%{name}
%{_sbindir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man8/*

