%if 0%{?rhel}
%global with_enca 0
%global with_libcue 0
%global with_rss 0
%else
%global with_enca 1
%global with_libcue 1
%global with_rss 1
%endif

%global tracker_version 2.1.0

%global systemd_units tracker-extract.service tracker-miner-apps.service tracker-miner-fs.service tracker-miner-rss.service tracker-writeback.service

Name:           tracker-miners
Version:        2.1.5
Release:        2%{?dist}.1
Summary:        Tracker miners and metadata extractors

# libtracker-extract is LGPLv2+; the miners are a mix of GPLv2+ and LGPLv2+ code
License:        GPLv2+ and LGPLv2+
URL:            https://wiki.gnome.org/Projects/Tracker
Source0:        https://download.gnome.org/sources/%{name}/2.1/%{name}-%{version}.tar.xz

Patch1:         backport-seccomp-improvements.diff

BuildRequires:  giflib-devel
BuildRequires:  intltool
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  systemd
BuildRequires:  vala
%if 0%{?with_enca}
BuildRequires:  pkgconfig(enca)
%endif
BuildRequires:  pkgconfig(exempi-2.0)
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(gexiv2)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:  pkgconfig(gstreamer-tag-1.0)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(icu-uc)
%if 0%{?with_libcue}
BuildRequires:  pkgconfig(libcue)
%endif
BuildRequires:  pkgconfig(libexif)
%if 0%{?with_rss}
BuildRequires:  pkgconfig(libgrss)
%endif
BuildRequires:  pkgconfig(libgsf-1)
BuildRequires:  pkgconfig(libgxps)
BuildRequires:  pkgconfig(libiptcdata)
BuildRequires:  pkgconfig(libosinfo-1.0)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libseccomp)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(poppler-glib)
BuildRequires:  pkgconfig(taglib_c)
BuildRequires:  pkgconfig(totem-plparser)
BuildRequires:  pkgconfig(tracker-sparql-2.0) >= %{tracker_version}
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(vorbisfile)

%{?systemd_requires}
Requires:       tracker%{?_isa} >= %{tracker_version}

# tracker-miners was split out from tracker in 1.99.2
Obsoletes:      tracker < 1.99.2
Conflicts:      tracker < 1.99.2

%description
Tracker is a powerful desktop-neutral first class object database,
tag/metadata database and search tool.

This package contains various miners and metadata extractors for tracker.


%prep
%autosetup -p1


%build
# Disable the functional tests for now, they use python bytecodes.
%configure --disable-static \
           --enable-libflac \
           --enable-libvorbis \
           --disable-mp3 \
           --disable-functional-tests \
           --disable-silent-rules
%make_build


%install
%make_install

find %{buildroot} -type f -name "*.la" -delete
rm -rf %{buildroot}%{_datadir}/tracker-tests

# Remove .so symlinks for private libraries -- no external users are supposed
# to link with them.
rm -f %{buildroot}%{_libdir}/tracker-miners-2.0/*.so

%find_lang %{name}


%post
%systemd_user_post %{systemd_units}

%preun
%systemd_user_preun %{systemd_units}

%postun
%systemd_user_postun_with_restart %{systemd_units}


%files -f %{name}.lang
%license COPYING
%doc AUTHORS NEWS README
%{_libdir}/tracker-miners-2.0/
%{_libexecdir}/tracker*
%{_datadir}/dbus-1/services/org.freedesktop.Tracker*
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/tracker/
%{_datadir}/tracker-miners/
%{_mandir}/man1/tracker-*.1*
%config(noreplace) %{_sysconfdir}/xdg/autostart/tracker*.desktop
%{_userunitdir}/tracker*.service


%changelog
* Wed Dec 06 2023 Carlos Garnacho <cgarnach@redhat.com> - 2.1.5-2.el8_9.1
- Fix issues and missing syscalls in seccomp improvements backport
  Resolves: RHEL-12465

* Tue Dec 05 2023 Carlos Garnacho <cgarnach@redhat.com> - 2.1.5-2
- Backport stricter seccomp jail
  Resolves: RHEL-12465

* Fri Sep 28 2018 Kalev Lember <klember@redhat.com> - 2.1.5-1
- Update to 2.1.5

* Wed Jul 25 2018 Kalev Lember <klember@redhat.com> - 2.1.0-1
- Update to 2.1.0

* Tue Jun 26 2018 Kalev Lember <klember@redhat.com> - 2.0.5-1
- Update to 2.0.5

* Sun Feb 11 2018 Sandro Mani <manisandro@gmail.com> - 2.0.4-3
- Rebuild (giflib)

* Thu Feb 08 2018 Kalev Lember <klember@redhat.com> - 2.0.4-2
- Rebuild to really enable the RAW extractor

* Wed Feb 07 2018 Kalev Lember <klember@redhat.com> - 2.0.4-1
- Update to 2.0.4
- Enable new gexiv2 based RAW extractor

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 2.0.3-2
- Rebuild for ICU 60.1

* Tue Nov 21 2017 Kalev Lember <klember@redhat.com> - 2.0.3-1
- Update to 2.0.3

* Fri Oct 06 2017 Kalev Lember <klember@redhat.com> - 2.0.2-1
- Update to 2.0.2

* Tue Sep 19 2017 Kalev Lember <klember@redhat.com> - 2.0.0-3
- Backport a fix for a crash when processing virtual elements (#1488707)

* Fri Sep 15 2017 Kalev Lember <klember@redhat.com> - 2.0.0-2
- Package review fixes (#1491725):
- Pass --disable-mp3 to use the generic gstreamer extractor
- Disable libstemmer support to match the previous behaviour
- Fix removing .so symlinks for private libraries
- Remove ldconfig rpm scripts as we don't install any shared libraries
- Correct license tag and add comment explaining mixed source licensing

* Thu Sep 14 2017 Kalev Lember <klember@redhat.com> - 2.0.0-1
- Initial Fedora packaging
