%global debug_package %{nil}

Name: snmptt
Version: 1.5
Release: 1%{?dist}
Summary: An SNMP trap handler written in Perl 

Group: System Environment/Daemons
License: GPLv2+
URL: http://www.snmptt.org/	
Source0: %{name}_%{version}.tar.gz
#TODO: Upstream
Source1: %{name}.service
Source2: convert-tar-gz-for-rpm.sh

BuildArch: noarch

Requires: net-snmp
Requires: logrotate
Requires: perl-Net-SNMP
Requires(pre): shadow-utils

%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:	systemd-units
Requires(post):	systemd-units
Requires(preun):	systemd-units
Requires(postun):	systemd-units
%else
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts
%endif

%description
SNMPTT (SNMP Trap Translator) is an SNMP trap handler written in Perl
for use with the Net-SNMP / UCD-SNMP snmptrapd program.  It can be
used to translate trap output from snmptrapd to more descriptive and
human friendly form, supports logging, invoking external programs, and
has the ability to accept or reject traps based on a number of
parameters.

%prep
%setup -q -n %{name}_%{version}

mv sample-*trap* examples/
mv examples/snmptt.conf.generic snmptt.conf

# convert ChangeLog to UTF-8
iconv -f ISO-8859-1 -t UTF-8 ChangeLog > ChangeLog.utf8 && \
touch -r ChangeLog ChangeLog.utf8 && \
mv -f ChangeLog{.utf8,}

%build

%install
install -D -p -m 0755 snmptt %{buildroot}%{_sbindir}/snmptt
install -D -p -m 0755 snmptthandler %{buildroot}%{_sbindir}/snmptthandler
install -D -p -m 0644 snmptthandler-embedded %{buildroot}%{_datadir}/snmptt/snmptthandler-embedded
install -D -p -m 0755 snmpttconvert %{buildroot}%{_bindir}/snmpttconvert
install -D -p -m 0755 snmpttconvertmib %{buildroot}%{_bindir}/snmpttconvertmib
install -D -p -m 0644 snmptt.conf %{buildroot}%{_sysconfdir}/snmp/snmptt.conf
install -D -p -m 0644 snmptt.ini %{buildroot}%{_sysconfdir}/snmp/snmptt.ini
%if 0%{?fedora} || 0%{?rhel} >= 7
install -D -p -m 0644 -p %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%else
install -D -p -m 0755 snmptt-init.d %{buildroot}%{_initrddir}/snmptt
%endif
install -D -p -m 0644 snmptt.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/snmptt
install -d -m 0755 %{buildroot}%{_localstatedir}/spool/snmptt
install -d -m 0755 %{buildroot}%{_localstatedir}/log/snmptt

%pre
getent group snmptt >/dev/null || groupadd -r snmptt
getent passwd snmptt >/dev/null || \
useradd -r -g snmptt -d /var/spool/snmptt -s /sbin/nologin \
-c "SNMP Trap Translator" snmptt
exit 0

%post
%if 0%{?fedora} || 0%{?rhel} >= 7
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%else
/sbin/chkconfig --add snmptt || :
%endif

%preun
if [ $1 -eq 0 ] ; then
%if 0%{?fedora} || 0%{?rhel} >= 7
  # Package removal, not upgrade
  /bin/systemctl --no-reload disable %{name}.service > /dev/null 2>&1 || :
  /bin/systemctl stop %{name}.service > /dev/null 2>&1 || :
%else
  /sbin/service snmptt stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del snmptt
%endif
fi

%postun
%if 0%{?fedora} || 0%{?rhel} >= 7
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi
%else
if [ $1 -ge 1 ] ; then
    %{_initrddir}/snmptt condrestart >/dev/null 2>&1 || :
fi
%endif


%files
%doc ChangeLog COPYING README
%doc contrib/ docs/ examples/
%{_sbindir}/snmptt
%{_sbindir}/snmptthandler
%{_datadir}/snmptt/
%{_bindir}/snmpttconvert
%{_bindir}/snmpttconvertmib
%config(noreplace) %{_sysconfdir}/snmp/snmptt.conf
%config(noreplace) %{_sysconfdir}/snmp/snmptt.ini
%config(noreplace) %{_sysconfdir}/logrotate.d/snmptt

%if 0%{?fedora} || 0%{?rhel} >= 7
%{_unitdir}/snmptt.service
%else
%{_initrddir}/snmptt
%endif

%attr(-,snmptt,snmptt) %dir %{_localstatedir}/spool/snmptt/
%attr(-,snmptt,snmptt) %dir %{_localstatedir}/log/snmptt/


%changelog
* Fri Nov 18 2022 Eliezer Croitoru <ngtech1ltd@gmail.com> - 1.5
- New upstream release

* Thu Jul 23 2020 Volker Fröhlich <volker27@gmx.at> - 1.4.2-1
- New upstream release

* Wed Jul 22 2020 Volker Fröhlich <volker27@gmx.at> - 1.4.1-1
- New upstream release

* Sat Jan 18 2014 Volker Fröhlich <volker27@gmx.at> - 1.4-0.9.beta2
- Correct permissions for embedded handler

* Sat Jan 18 2014 Volker Fröhlich <volker27@gmx.at> - 1.4-0.8.beta2
- Add embedded trap handler (BZ 1038596)
- Simplify if clauses for Fedora
- Remove defattr, clean section and initial rm in install section

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-0.7.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Andrew Colin Kissa <andrew@topdog.za.net> - 1.4-0.6.beta2
- Require perl-Net-SNMP

* Mon Oct 29 2012 Andrew Colin Kissa <andrew@topdog.za.net> - 1.4-0.5.beta2
- Fixes requested by reviewer

* Sun Oct 28 2012 Andrew Colin Kissa <andrew@topdog.za.net> - 1.4-0.4.beta2
- Fix incorrect files

* Sun Oct 28 2012 Andrew Colin Kissa <andrew@topdog.za.net> - 1.4-0.3.beta2
- Added shadow-utils dependency

* Sun Oct 28 2012 Andrew Colin Kissa <andrew@topdog.za.net> - 1.4-0.2.beta2
- Fix issues raised by reviewer

* Thu Oct 25 2012 Andrew Colin Kissa <andrew@topdog.za.net> - 1.4-0.1.beta2
- New upstream release.
- Fedora review changes implemented
- Introduce systemd files

* Mon Jul 27 2009 Gary T. Giesen <giesen@snickers.org> 1.3-0.1.beta2
- New upstream release. Incorporates previous fixes from Ville Skysttä

* Mon Jul 07 2009 Gary T. Giesen <giesen@snickers.org> 1.2-3
- Incorporated various patches and suggestions from Ville Skysttä 
<ville.skytta at iki.fi>

* Mon Jul 07 2009 Gary T. Giesen <giesen@snickers.org> 1.2-2
- Spec file cleanup

* Mon Jul 06 2009 Gary T. Giesen <giesen@snickers.org> 1.2-1
- Initial spec file creation
