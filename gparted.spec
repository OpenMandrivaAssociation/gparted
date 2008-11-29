Summary:    Graphical frontend to libparted
Name:       gparted
Version:    0.4.0
Release:    %mkrel 1
License:    GPLv2+
Group:      System/Kernel and hardware      

Source0:    http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:    run-gparted
Source2:    gparted-console.apps
Source3:    gparted-pam.d
Patch102:   gparted-realpath-fix.patch
Patch103:   gparted-refresh_crash-fix.patch
Url:        http://gparted.sourceforge.net
BuildRoot:  %_tmppath/%name-%version-root
BuildRequires:  parted-devel >= 1.6.13 
BuildRequires:  gtkmm2.4-devel
BuildRequires:  ImageMagick
BuildRequires:	desktop-file-utils
BuildRequires:	gnome-doc-utils
Requires:   usermode-consoleonly

%description
GParted stands for Gnome Partition Editor and is a graphical frontend to 
libparted. Among other features it supports creating, resizing, moving 
and copying of partitions.

%prep
%setup -q
%patch102 -p0 -b .realpath
%patch103 -p0 -b .refresh

%build
%configure2_5x
%make

%install
rm -fr %buildroot
%makeinstall_std
%find_lang %name

# Create a helper script to launch gparted using hal-lock
mkdir -p %buildroot%_bindir
cp %{SOURCE1} %{buildroot}%{_bindir}/
chmod 755 %{buildroot}%{_bindir}/run-gparted

#consolehelper
ln -sf consolehelper $RPM_BUILD_ROOT%{_bindir}/gparted

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/security/console.apps/gparted

mkdir -p %{buildroot}%{_sysconfdir}/pam.d
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/gparted

desktop-file-install --vendor='' \
	--dir %buildroot%_datadir/applications/ \
	--add-category='GTK;HardwareSettings;Settings' \
	%buildroot%_datadir/applications/*.desktop

%clean
rm -fr %buildroot

%preun
if [ $1 -ge 0 ]; then
    if [ -a %{_datadir}/hal/fdi/policy/gparted-disable-automount.fdi ]; then
       rm -rf %{_datadir}/hal/fdi/policy/gparted-disable-automount.fdi
    fi
fi

%if %mdkversion < 200900
%post
%update_menus
%endif
                
%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS README COPYING ChangeLog
%{_bindir}/%{name}
%{_bindir}/run-gparted
%{_sbindir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_mandir}/man8/*
%{_datadir}/gnome/help/%{name}/*/%{name}.xml
%{_datadir}/omf/%{name}/%{name}-*.omf
%config(noreplace) %{_sysconfdir}/pam.d/gparted
%config(noreplace) %{_sysconfdir}/security/console.apps/gparted
