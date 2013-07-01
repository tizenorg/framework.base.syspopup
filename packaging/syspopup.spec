Name:       syspopup
Summary:    syspopup package
Version:    0.0.97
Release:    1
Group:      System/Libraries
License:    Apache License, Version 2.0
Source0:    syspopup-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(utilX)
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(evas)
BuildRequires:  pkgconfig(appcore-efl)


%description
syspopup package for popup


%package devel
Summary:    syspopup development package
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
syspopup development package popup

%package caller
Summary:    syspopup-caller package
Group:      TO_BE/FILLED_IN
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description caller
syspopup-caller package for popup

%package caller-devel
Summary:    syspopup-caller development package
Group:      TO_BE/FILLED_IN
Requires:   %{name} = %{version}-%{release}

%description caller-devel
syspopup-caller development package for popup

%package app
Summary:    org.tizen.syspopup-app test app
Group:      TO_BE/FILLED_IN
Requires:   %{name} = %{version}-%{release}

%description app
org.tizen.syspopup-app test app package

%prep
%setup -q

%build
%cmake . -DEXTRA_CFLAGS=-fPIC

make %{?jobs:-j%jobs}

%install
%make_install

mkdir -p %{buildroot}/opt/dbspace
sqlite3 %{buildroot}/opt/dbspace/.syspopup.db < %{buildroot}/usr/share/syspopup/syspopup_db.sql
rm -rf %{buildroot}/usr/share/syspopup/syspopup_db.sql

touch %{buildroot}%{_datadir}/popup_noti_term

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post caller -p /sbin/ldconfig

%postun caller -p /sbin/ldconfig

%files
%manifest syspopup.manifest
%defattr(-,root,root,-)
%{_libdir}/libsyspopup.so.0.1.0
%{_datadir}/popup_noti_term
%attr(644,root,app) /opt/dbspace/.syspopup.db
%attr(644,root,app) /opt/dbspace/.syspopup.db-journal
%{_bindir}/sp_test

%files devel
%defattr(-,root,root,-)
%{_includedir}/SLP_SYSPOPUP_PG.h
%{_includedir}/syspopup.h
%{_libdir}/libsyspopup.so
%{_libdir}/pkgconfig/syspopup.pc

%files caller
%manifest syspopup-caller.manifest
%defattr(-,root,root,-)
%{_libdir}/libsyspopup_caller.so.0.1.0

%files caller-devel
%defattr(-,root,root,-)
%{_libdir}/libsyspopup_caller.so
%{_includedir}/syspopup_caller.h
%{_libdir}/pkgconfig/syspopup-caller.pc

%files app
%manifest org.tizen.syspopup-app.manifest
%defattr(-,root,root,-)
%{_datadir}/icons/default/small/org.tizen.syspopup-app.png
%{_bindir}/syspopup-app
/usr/share/packages/org.tizen.syspopup-app.xml

%changelog
* Fri Jun 21 2013 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Change end key term info of wifi-qs

* Fri Apr 12 2013 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Remove drm syspopup requested by hakjoo.ko

* Tue Apr 2 2013 - Hyugdeuk Kim <hd3.kim@samsung.com>
- Add syspopup_reset_timeout api
