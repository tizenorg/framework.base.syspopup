Name:       syspopup
Summary:    syspopup package
Version:    0.0.122
Release:    1
Group:      System/Libraries
License:    Apache License, Version 2.0
Source0:    syspopup-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(post): /bin/touch
Requires(postun): /sbin/ldconfig
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

%if 0%{?tizen_profile_mobile}
%package app
Summary:    org.tizen.syspopup-app test app
Group:      TO_BE/FILLED_IN
Requires:   %{name} = %{version}-%{release}

%description app
org.tizen.syspopup-app test app package
%endif

%prep
%setup -q -n %{name}-%{version}

%build
%if 0%{?tizen_profile_wearable}
%if 0%{?tizen_build_binary_release_type_eng}
export CFLAGS="$CFLAGS -DTIZEN_ENGINEER_MODE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_ENGINEER_MODE"
export FFLAGS="$FFLAGS -DTIZEN_ENGINEER_MODE"
%endif
cd wearable
export CFLAGS="$CFLAGS -Wall -Werror -Wno-unused-function"
CFLAGS=${_cflags} cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DEXTRA_CFLAGS=-fPIC

make %{?jobs:-j%jobs}

%else
cd mobile
%cmake . -DEXTRA_CFLAGS=-fPIC

make %{?jobs:-j%jobs}
%endif
%install
%if 0%{?tizen_profile_wearable}
rm -rf %{buildroot}
cd wearable
%make_install

mkdir -p %{buildroot}/opt/dbspace
sqlite3 %{buildroot}/opt/dbspace/.syspopup.db < %{buildroot}/usr/share/syspopup/syspopup_db.sql
rm -rf %{buildroot}/usr/share/syspopup/syspopup_db.sql

touch %{buildroot}%{_datadir}/popup_noti_term

mkdir -p %{buildroot}/usr/share/license
cp LICENSE %{buildroot}/usr/share/license/%{name}
cp LICENSE %{buildroot}/usr/share/license/%{name}-caller
%else
rm -rf %{buildroot}
cd mobile
%make_install
mkdir -p %{buildroot}/usr/share/license
install LICENSE %{buildroot}/usr/share/license/%{name}
install LICENSE %{buildroot}/usr/share/license/%{name}-devel
install LICENSE %{buildroot}/usr/share/license/%{name}-caller
install LICENSE %{buildroot}/usr/share/license/%{name}-caller-devel
install LICENSE %{buildroot}/usr/share/license/%{name}-app

mkdir -p %{buildroot}/opt/dbspace
sqlite3 %{buildroot}/opt/dbspace/.syspopup.db < %{buildroot}/usr/share/syspopup/syspopup_db.sql
rm -rf %{buildroot}/usr/share/syspopup/syspopup_db.sql

touch %{buildroot}%{_datadir}/popup_noti_term
%endif
%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%post caller -p /sbin/ldconfig

%postun caller -p /sbin/ldconfig

%files
%if 0%{?tizen_profile_mobile}
%manifest mobile/syspopup.manifest
%else
%manifest wearable/syspopup.manifest
%endif
%defattr(-,root,root,-)
%{_libdir}/libsyspopup.so.0.1.0
%{_datadir}/popup_noti_term
%attr(644,root,app) /opt/dbspace/.syspopup.db
%attr(644,root,app) /opt/dbspace/.syspopup.db-journal
%{_bindir}/sp_test
/usr/share/license/%{name}

%files devel
%defattr(-,root,root,-)
%{_includedir}/SLP_SYSPOPUP_PG.h
%{_includedir}/syspopup.h
%{_libdir}/libsyspopup.so
%{_libdir}/pkgconfig/syspopup.pc
%if 0%{?tizen_profile_mobile}
/usr/share/license/%{name}-devel
%endif

%files caller
%if 0%{?tizen_profile_mobile}
%manifest mobile/syspopup-caller.manifest
%else
%manifest wearable/syspopup-caller.manifest
%endif
%defattr(-,root,root,-)
%{_libdir}/libsyspopup_caller.so.0.1.0
/usr/share/license/%{name}-caller

%files caller-devel
%defattr(-,root,root,-)
%{_libdir}/libsyspopup_caller.so
%{_includedir}/syspopup_caller.h
%{_libdir}/pkgconfig/syspopup-caller.pc
%if 0%{?tizen_profile_mobile}
/usr/share/license/%{name}-caller-devel

%files app
%manifest mobile/org.tizen.syspopup-app.manifest
%defattr(-,root,root,-)
%{_datadir}/icons/default/small/org.tizen.syspopup-app.png
%{_bindir}/syspopup-app
/usr/share/packages/org.tizen.syspopup-app.xml
/usr/share/license/%{name}-app
%endif

%changelog
* Tue Feb 18 2014 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Remove unused system popup sample app
- Remove unused debian folder

* Wed Jan 15 2014 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Add fota syspopup
- Requested by seokey.jeong

* Fri Sep 13 2013 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Add crash system popup
- Requested by ty317.kim

* Tue Sep 10 2013 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Remove unused ticker noti system popup
- Maintained by sungho1.kwak
- Add Wall, Werror build option

* Fri Jun 21 2013 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Change end key term info for wifi-qs popup

* Wed Jun 5 2013 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Add datausage system popup
- Requested by ty317.kim

* Fri May 17 2013 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Add safety volume popup
- Requested by bw.jang

* Tue Apr 30 2013 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Change focus value to 0 for power-off syspopup
- Requested by ty317.kim

* Thu Apr 25 2013 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Change prio info for system , power-off syspopup
- Requested by ty317.kim

* Wed Apr 24 2013 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Add system-syspopup 
- Requested by ty317.kim

* Fri Apr 12 2013 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Remove drm syspopup 
- Requested by hakjoo.ko

* Tue Apr 2 2013 - Hyugdeuk Kim <hd3.kim@samsung.com>
- Add syspopup_reset_timeout api

* Thu Mar 28 2013 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Add sym extraction syspopup info(telephony-syspopup)
- Requested by jh48.an

* Mon Mar 25 2013 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Add mobileap syspopup
- Requested by sy39.ju

* Thu Feb 21 2013 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Add syspopup app smack rule
- Change dlog tag
- Add dlogs for debug

* Wed Nov 21 2012 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Add syspopup info for gcf supl

* Tue Oct 30 2012 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Fix prevent issues
- Add syspopup info for hdmi syspopup
- move CFLAGS location to %build at spec file
