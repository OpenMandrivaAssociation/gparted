Summary:    Graphical frontend to libparted
Name:       gparted
Version:    0.3.6
Release:    %mkrel 1
License:    GPLv2+
Group:      System/Kernel and hardware      

Source0:    http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:    run-gparted
Source2:    gparted-console.apps
Source3:    gparted-pam.d
Patch0:     gparted-0.3.3-desktop.patch
Patch100:   gparted-dont-lock-hal.patch
Patch102:   gparted-realpath-fix.patch
Patch103:   gparted-refresh_crash-fix.patch
Url:        http://gparted.sourceforge.net
BuildRoot:  %_tmppath/%name-%version-root
BuildRequires:  parted-devel >= 1.6.13 
BuildRequires:  gtkmm2.4-devel
BuildRequires:  ImageMagick
Requires:   usermode-consoleonly

%description
GParted stands for Gnome Partition Editor and is a graphical frontend to 
libparted. Among other features it supports creating, resizing, moving 
and copying of partitions.

%prep
%setup -q
%patch0 -p0
%patch100 -p0 -b .hal
%patch102 -p0 -b .realpath
%patch103 -p0 -b .refresh

%build
%configure2_5x
%make

%install
rm -fr %buildroot
%makeinstall_std
%find_lang %name

#icons
mkdir -p $RPM_BUILD_ROOT/{%_liconsdir,%_iconsdir,%_miconsdir}
convert pixmaps/%{name}.png -geometry 32x32 %{buildroot}%{_iconsdir}/%{name}.png
install pixmaps/%{name}.png %{buildroot}%{_liconsdir}/%{name}.png
convert pixmaps/%{name}.png -geometry 16x16 %{buildroot}%{_miconsdir}/%{name}.png

# Create a helper script to launch gparted using hal-lock
cp %{SOURCE1} %{buildroot}%{_bindir}/
chmod 755 %{buildroot}%{_bindir}/run-gparted

#consolehelper
install -d $RPM_BUILD_ROOT%{_sbindir}
mv $RPM_BUILD_ROOT%{_bindir}/gparted $RPM_BUILD_ROOT%{_sbindir}
ln -sf consolehelper $RPM_BUILD_ROOT%{_bindir}/gparted

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/security/console.apps/gparted

mkdir -p %{buildroot}%{_sysconfdir}/pam.d
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/gparted

%clean
rm -fr %buildroot

%preun
if [ $1 -ge 0 ]; then
    if [ -a %{_datadir}/hal/fdi/policy/gparted-disable-automount.fdi ]; then
       rm -rf %{_datadir}/hal/fdi/policy/gparted-disable-automount.fdi
    fi
fi

%post
%update_menus
                
%postun
%clean_menus

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS README COPYING ChangeLog
%{_bindir}/%{name}
%{_bindir}/run-gparted
%{_sbindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/pixmaps/%{name}.png
%config(noreplace) %{_sysconfdir}/pam.d/gparted
%config(noreplace) %{_sysconfdir}/security/console.apps/gparted
