Summary:    GParted is a graphical frontend to libparted
Name:       gparted
Version:    0.3.3
Release:    %mkrel 5
License:    GPL
Group:      System/Kernel and hardware      

Source:     http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0:     gparted-0.3.3-desktop.patch
Url:        http://%{name}.sourceforge.net/
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

%build
%configure2_5x
%make

%install
rm -fr %buildroot
%makeinstall
%find_lang %name

#icons
mkdir -p $RPM_BUILD_ROOT/{%_liconsdir,%_iconsdir,%_miconsdir}
convert pixmaps/%{name}.png -geometry 32x32 %{buildroot}%{_iconsdir}/%{name}.png
install pixmaps/%{name}.png %{buildroot}%{_liconsdir}/%{name}.png
convert pixmaps/%{name}.png -geometry 16x16 %{buildroot}%{_miconsdir}/%{name}.png

#consolehelper
install -d $RPM_BUILD_ROOT%{_sbindir}
mv $RPM_BUILD_ROOT%{_bindir}/gparted $RPM_BUILD_ROOT%{_sbindir}
pushd $RPM_BUILD_ROOT%{_bindir}
ln -sf consolehelper %{name}
popd

%clean
rm -fr %buildroot

%post
%update_menus
                
%postun
%clean_menus

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS README COPYING ChangeLog
%{_bindir}/%{name}
%{_sbindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/pixmaps/%{name}.png
