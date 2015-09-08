
Name:       syspopup
Summary:    syspopup package
Version:    0.0.134
Release:    1
Group:      System/Libraries
License:    Apache-2.0
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
BuildRequires:  pkgconfig(capi-appfw-application)

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
%setup -q -n %{name}-%{version}

%build
%if "%{?tizen_profile_name}" == "wearable"
export CFLAGS="$CFLAGS –D_WEARABLE"
%else
export CFLAGS="$CFLAGS -D_MOBILE"
%endif

%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif
export CFLAGS="$CFLAGS -Wall -Werror -Wno-unused-function"
CFLAGS=${_cflags} cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DEXTRA_CFLAGS=-fPIC \
	-D_WEARABLE:BOOL=${_WEARABLE} -D_MOBILE:BOOL=${_MOBILE} \
	.

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}/opt/dbspace
sqlite3 %{buildroot}/opt/dbspace/.syspopup.db < %{buildroot}/usr/share/syspopup/syspopup_db.sql
rm -rf %{buildroot}/usr/share/syspopup/syspopup_db.sql

mkdir -p %{buildroot}/usr/share/license
cp LICENSE %{buildroot}/usr/share/license/%{name}
cp LICENSE %{buildroot}/usr/share/license/%{name}-caller

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%post caller -p /sbin/ldconfig

%postun caller -p /sbin/ldconfig

%files
%manifest syspopup.manifest
%defattr(-,root,root,-)
%{_libdir}/libsyspopup.so.0.1.0
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

%files caller
%manifest syspopup-caller.manifest
%defattr(-,root,root,-)
%{_libdir}/libsyspopup_caller.so.0.1.0
/usr/share/license/%{name}-caller

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
/etc/smack/accesses2.d/org.tizen.syspopup-app.rule

%changelog
* Fri Aug 1 2014 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Change focus info of safetysyspopup
- Requested by nannan.wu , parkjg

* Thu May 22 2014 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Change timeout info of wc syspopup
- Requested by sunil85.kim

* Thu May 22 2014 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Change focus info of mode syspopup
- Requested by setting

* Mon May 19 2014 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Add root detection popup
- Requested by daehoon ko of security r&d group

* Mon May 12 2014 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Add setting noti popup for blocking mode

* Thu May 8 2014 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Remove code to grab back key for volume popup

* Mon Apr 28 2014 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Add wc syspopup requested by ms0123.kim of telephony team

* Mon Mar 31 2014 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Enable telephony syspopup following telephony build feature

* Tue Feb 18 2014 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Remove unused system popup sample app
- Remove unused debian folder

* Wed Jan 15 2014 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Add fota syspopup
- Requested by seokey.jeong

* Tue Dec 10 2013 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Add fota-noti popup
- Requested by juhaki.park

* Wed Oct 23 2013 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Add fus-ode-syspopup
- Requested by sunbong.ha

* Fri Oct 18 2013 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Add keepit screen capture system popup
- Requested by wc0917.lee

* Thu Oct 10 2013 - Hyungdeuk Kim <hd3.kim@samsung.com>
- Add mode system popup
- Requested by shy81.shin

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
