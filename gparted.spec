%define _files_listed_twice_terminate_build 0

Summary:	Graphical frontend to libparted
Name:		gparted
Version:	0.12.0
Release:	%mkrel 2
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://gparted.sourceforge.net
Source0:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source2:	gparted-console.apps
Source3:	gparted-pam.d
BuildRequires:	parted-devel >= 1.7.1
BuildRequires:	libuuid-devel
BuildRequires:	gtkmm2.4-devel
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
BuildRequires:	gnome-doc-utils
BuildRequires:	intltool
BuildRequires:	sigc++2.0-devel
Requires:	usermode-consoleonly

%description
GParted stands for Gnome Partition Editor and is a graphical frontend to 
libparted. Among other features it supports creating, resizing, moving 
and copying of partitions.

%prep
%setup -q

%build
# fwang: autoreconf is needed, otherwise old version of intltool shipped with tarball will be used
autoreconf -fi
%configure2_5x --enable-libparted-dmraid
%make

%install
%__rm -fr %{buildroot}
%makeinstall_std
%find_lang %{name} --with-gnome

#consolehelper
%__mkdir_p %{buildroot}%{_bindir}
%__ln_s consolehelper %{buildroot}%{_bindir}/gparted
%__sed -i 's|%{_sbindir}|%{_bindir}|' %{buildroot}%{_datadir}/applications/*.desktop

%__mkdir_p %{buildroot}%{_sysconfdir}/security/console.apps
%__cp %{SOURCE2} %{buildroot}%{_sysconfdir}/security/console.apps/gparted

%__mkdir_p %{buildroot}%{_sysconfdir}/pam.d
%__cp %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/gparted

desktop-file-install --vendor='' \
	--dir %{buildroot}%{_datadir}/applications/ \
	--remove-category=GNOME \
	--add-category='GTK;HardwareSettings;Settings' \
	%{buildroot}%{_datadir}/applications/*.desktop

%clean
%__rm -fr %{buildroot}

%preun
if [ $1 -ge 0 ]; then
    if [ -a %{_datadir}/hal/fdi/policy/gparted-disable-automount.fdi ]; then
       rm -rf %{_datadir}/hal/fdi/policy/gparted-disable-automount.fdi
    fi
fi

%files -f %{name}.lang
%doc AUTHORS README COPYING ChangeLog
%{_bindir}/%{name}
%{_sbindir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man8/*
%{_datadir}/omf/%{name}/
%config(noreplace) %{_sysconfdir}/pam.d/gparted
%config(noreplace) %{_sysconfdir}/security/console.apps/gparted
