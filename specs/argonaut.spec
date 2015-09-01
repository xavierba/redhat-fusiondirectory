Name:		argonaut
Version:	_VERSION_	
Release:	_RELEASE_
Summary:	Tool to convert schema into ldif format

Group:		Applications/System
License:	BSD
URL:		https://forge.fusiondirectory.org/projects/%{name}

Source0:	%{name}-%{version}.tar.gz
Source1:        %{name}-client.init
Source2:        %{name}-fuse.init
Source3:        %{name}-server.init
Source4:        %{name}-client.default
Source5:        %{name}-server.default
Source6:        %{name}-fuse.logrotate
Source7:        %{name}-fai-monitor.init

Patch0:         %{name}-fix-ldap-directory.patch

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch
BuildRequires: 	wget

%description
Argonaut json rpc server to manage deployment system

%package client
Summary:        Argonaut json rpc server to manage deployment system
Requires:	%{name}-common, perl-Config-IniFiles, perl-Log-Handler, perl-File-Pid, perl-App-Daemon
Requires:	perl-JSON >= 2.07-1, perl-JSON-RPC, redhat-lsb-core
%description client
Argonaut client to manage computers and services.

%package common
Summary:        Argonaut common functions and librairies
Requires:	coreutils >= 6.10-1, openldap-clients
Requires:	perl-IO-Socket-SSL, perl-Path-Class, perl-LDAP, perl-Digest-SHA
%description common
Common perl libraries used by the Argonaut deployment system.

%package common-fai
Summary:        Argonaut common library for FAI
Requires:	coreutils >= 6.10-1, %{name}-common, openldap-clients, perl-IO-Socket-SSL
Requires: 	perl-Net-LDAP-Server, perl-Path-Class
%description common-fai
Library for FAI (Fully Automated install) used by the Argonaut deployment system.

%package dovecot
Summary:        Argonaut client-module for dovecot
%description dovecot
Argonaut client module to manage the creation of the directory for the user where is mailbox is created.

%package fai-monitor
Summary:        argonaut-fai-monitor - read status of installation and send information to argonaut-server for FusionDirectory
Requires:	%{name}-client
%description fai-monitor
argonaut-fai-monitor replaces fai-monitor and send information to argonaut-server for FusionDirectory to show them in deployment queue

%package fuse
Summary:        Modular TFTP/Fuse supplicant
Requires:	%{name}-common, perl-Log-Handler, perl-Config-IniFiles, perl-Fuse
Requires:	perl-File-Pid, perl-Net-LDAP-Server, redhat-lsb-core
#Requires:      ucf, fuse-utils
%description fuse
Argonaut-fuse is a modular fuse-tftp-supplicant written in perl which allows
to create pxelinux configurations for different types of clients using external modules

%package fuse-module-fai
Summary:        LDAP FAI module for the TFTP/Fuse supplicant
Requires:      %{name}-fuse
%description fuse-module-fai
FAI module for argonaut-fuse which is using the LDAP backend in conjunction
with FusionDirectory and Argonaut to generate client configurations.

%package fuse-module-opsi
Summary:        LDAP FAI module for the TFTP/Fuse supplicant
Requires:      %{name}-fuse
%description fuse-module-opsi
FAI module for argonaut-fuse which is using the LDAP backend in conjunction
with FusionDirectory and Argonaut to generate client configurations.

%package ldap2zone
Summary:        Argonaut tool to extract DNS zones from LDAP trees
Requires:	%{name}-common, perl-Config-IniFiles, perl-Net-LDAP-Server, perl-DNS-ZoneParse >= 1.10
Conflicts:	ldap2zone
%description ldap2zone
This is a tool that reads info for a zone from LDAP and constructs
a standard plain ascii zone file. The LDAP information has to be
stored using the dnszone schema.

%package quota
Summary:        Argonaut tool to apply disk quota from ldap
Requires:	%{name}-common, perl-Config-IniFiles, perl-Net-LDAP-Server, perl-Quota, quota
%description quota
This is a tool that reads info for quota from LDAP and apply it
to your quota server. The LDAP information has to be stored using
the fdQuota schema.

%package server
Summary:        Argonaut json rpc server to manage deployment system
Requires:	%{name}-common
Requires:	perl-DateTime, perl-LDAP, perl-Log-Handler, perl-POE-Component-Schedule
Requires:	perl-POE-Component-Server-SimpleHTTP
Requires:	perl-POE-Component-Pool-Thread, perl-POE-Component-Server-JSONRPC
Requires:	perl-JSON-RPC, perl-File-Pid, perl-App-Daemon, perl-JSON >= 2.07-1
Requires:	perl-Config-IniFiles, perl-POE, perl-POE-Component-SSLify, redhat-lsb-core
%description server
Argonaut server to manage deployment systems.

%package server-module-fai
Summary:        Argonaut json rpc server module to manage FAI (Fully Automated Install)
Requires:	%{name}-server
%description server-module-fai
Argonaut server module to manage FAI (Fully Automated Install) installation.

%package server-module-opsi
Summary:        Argonaut json rpc server module to manage OPSI installation
Requires:       %{name}-server
%description server-module-opsi
Argonaut server module to manage OPSI installation.

%package yumgroup2yumi
Summary:        Command to convert yumgroup to yumi for FAI classes
%description yumgroup2yumi
Command that convert yumgroup in yumi for FAI classes

%prep
%setup -q -n %{name}-%{version}
%patch0

# Manpages in gz
gzip ./%{name}-server/man/%{name}-server.1
gzip ./%{name}-client/man/%{name}-client.1
gzip ./%{name}-ldap2zone/man/%{name}-ldap2zone.1
gzip ./%{name}-quota/man/%{name}-quota.1
gzip ./%{name}-fuse/man/%{name}-fuse.1
gzip ./%{name}-fai-monitor/man/%{name}-fai-monitor.1
gzip ./%{name}-fai-server/man/yumgroup2yumi.1

%build

%install
# Clean buildroot before install
rm -rf %{buildroot} 

# Directories
mkdir -p %{buildroot}/%{_sbindir}/
mkdir -p %{buildroot}/%{_datadir}/perl5/
mkdir -p %{buildroot}/%{_datadir}/man1/
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/
mkdir -p %{buildroot}/%{_sysconfdir}/init.d/
mkdir -p %{buildroot}/%{_sysconfdir}/default/
mkdir -p %{buildroot}/usr/lib/fai/
mkdir -p %{buildroot}/%{_sysconfdir}/fai/nfsroot-hooks/
mkdir -p %{buildroot}/%{_datadir}/perl5/Argonaut/Fuse/Modules/
mkdir -p %{buildroot}/%{_datadir}/perl5/Argonaut/Server/Modules/
mkdir -p %{buildroot}/%{_datadir}/perl5/Argonaut/ClientDaemon/Modules/
mkdir -p %{buildroot}/%{_datadir}/perl5/Argonaut/Libraries/
mkdir -p %{buildroot}/%{_sysconfdir}/init.d/*

# Copy init files
cp %{S:1} %{buildroot}/%{_sysconfdir}/init.d/%{name}-client
cp %{S:2} %{buildroot}/%{_sysconfdir}/init.d/%{name}-fuse
cp %{S:3} %{buildroot}/%{_sysconfdir}/init.d/%{name}-server
cp %{S:7} %{buildroot}/%{_sysconfdir}/init.d/%{name}-fai-monitor

# Copy default files
cp %{S:4} %{buildroot}/%{_sysconfdir}/default/%{name}-client
cp %{S:5} %{buildroot}/%{_sysconfdir}/default/%{name}-server

# Install argonaut-server-module-fai and argonaut-server-module-opsi
cd ./%{name}-server
cp ./Argonaut/Server/Modules/FAI.pm %{buildroot}/%{_datadir}/perl5/Argonaut/Server/Modules/
cp ./Argonaut/Server/Modules/OPSI.pm %{buildroot}/%{_datadir}/perl5/Argonaut/Server/Modules/

# Install argonaut-server
cp ./bin/* %{buildroot}/%{_sbindir}/
cp -a ./Argonaut/ %{buildroot}/%{_datadir}/perl5/
cp ./man/%{name}-server.1.gz %{buildroot}/%{_datadir}/man1/
cd ..

# Install argonaut-client
cd ./%{name}-client
cp ./bin/* %{buildroot}/%{_sbindir}/
cp ./Argonaut/ClientDaemon.pm %{buildroot}/%{_datadir}/perl5/Argonaut/
cp ./Argonaut/ClientDaemon/Modules/Service.pm %{buildroot}/%{_datadir}/perl5/Argonaut/ClientDaemon/Modules/
cp ./Argonaut/ClientDaemon/Modules/System.pm  %{buildroot}/%{_datadir}/perl5/Argonaut/ClientDaemon/Modules/
cp ./man/%{name}-client.1.gz %{buildroot}/%{_datadir}/man1/
cd ..

# Install argonaut-common
cd ./%{name}-common
cp ./Argonaut/Libraries/Common.pm  %{buildroot}/%{_datadir}/perl5/Argonaut/Libraries/
cp ./Argonaut/Libraries/Packages.pm %{buildroot}/%{_datadir}/perl5/Argonaut/Libraries/
cp ./%{name}.conf %{buildroot}/%{_sysconfdir}/%{name}/

# Install argonaut-common-fai
cp ./Argonaut/Libraries/FAI.pm %{buildroot}/%{_datadir}/perl5/Argonaut/Libraries/
cd ..

# Install argonaut-dovecot
cd ./%{name}-dovecot
cp ./Argonaut/ClientDaemon/Modules/Dovecot.pm %{buildroot}/%{_datadir}/perl5/Argonaut/ClientDaemon/Modules/
cd ..

# Install argonaut-fai-monitor and argonaut-yumgroup2youmi
cd ./%{name}-fai-server
cp ./bin/{argonaut-fai-monitor,yumgroup2yumi} %{buildroot}/%{_sbindir}/
cp ./man/{argonaut-fai-monitor.1.gz,yumgroup2yumi.1.gz} %{buildroot}/%{_datadir}/man1/
cd .. 

# Install argonaut-fuse-module-fai
cd ./%{name}-fuse
cp ./Argonaut/Fuse/Modules/FAI.pm  %{buildroot}/%{_datadir}/perl5/Argonaut/Fuse/Modules/

# Install argonaut-fuse-module-opsi
cp ./Argonaut/Fuse/Modules/OPSI.pm  %{buildroot}/%{_datadir}/perl5/Argonaut/Fuse/Modules/

# Install argonaut-fuse
cp ./bin/%{name}-fuse %{buildroot}/%{_sbindir}/
cp ./man/%{name}-fuse.1.gz %{buildroot}/%{_datadir}/man1/

# Logrotate config
mkdir -p %{buildroot}/etc/logrotate.d/
cp %{S:6} %{buildroot}/etc/logrotate.d/%{name}-fuse
cd ..

# Install argonaut-ldap2zone
cd ./%{name}-ldap2zone
cp ./bin/* %{buildroot}/%{_sbindir}/
cp -a ./Argonaut/ %{buildroot}/%{_datadir}/perl5/
cp ./man/%{name}-ldap2zone.1.gz %{buildroot}/%{_datadir}/man1/
cd ..

# Install argonaut-quota
cd ./%{name}-quota
cp ./bin/* %{buildroot}/%{_sbindir}/
cp -a ./Argonaut/ %{buildroot}/%{_datadir}/perl5/
cp ./man/%{name}-quota.1.gz %{buildroot}/%{_datadir}/man1/
cd ..

# Set the good rights
chmod +x %{buildroot}/%{_sbindir}/*
chmod +x %{buildroot}/%{_sysconfdir}/init.d/*

%clean
rm -rf %{buildroot} 

%files client
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
%{_sysconfdir}/init.d/%{name}-client
%{_sysconfdir}/default/%{name}-client
%{_sbindir}/%{name}-client
%{_datadir}/perl5/Argonaut/ClientDaemon.pm 
%{_datadir}/perl5/Argonaut/ClientDaemon/Modules/Service.pm
%{_datadir}/perl5/Argonaut/ClientDaemon/Modules/System.pm
%{_datadir}/man1/%{name}-client.1.gz

%files common
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
%{_sysconfdir}/%{name}/%{name}.conf
%{_datadir}/perl5/Argonaut/Libraries/Common.pm
%{_datadir}/perl5/Argonaut/Libraries/Packages.pm 

%files ldap2zone
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
%{_sbindir}/%{name}-ldap2zone
%{_datadir}/perl5/Argonaut/Libraries/Ldap2zone.pm 
%{_datadir}/perl5/Argonaut/ClientDaemon/Modules/Ldap2Zone.pm
%{_datadir}/man1/%{name}-ldap2zone.1.gz

%files quota
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
%{_sbindir}/%{name}-quota
%{_datadir}/perl5/Argonaut/Libraries/Quota.pm
%{_datadir}/man1/%{name}-quota.1.gz

%files server
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
%{_sysconfdir}/init.d/%{name}-server
%{_sysconfdir}/default/%{name}-server
%{_sbindir}/%{name}-server
%{_datadir}/perl5/Argonaut/Server/ModulesPool.pm
%{_datadir}/perl5/Argonaut/Server/Modules/Argonaut.pm
%{_datadir}/perl5/Argonaut/Server/Modules/OPSI.pm
%{_datadir}/man1/%{name}-server.1.gz

%files fuse-module-fai
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
%{_datadir}/man1/%{name}-fuse.1.gz
%{_datadir}/perl5/Argonaut/Fuse/Modules/FAI.pm

%files fuse-module-opsi
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
%{_datadir}/man1/%{name}-fuse.1.gz
%{_datadir}/perl5/Argonaut/Fuse/Modules/OPSI.pm

%files fuse
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
%{_sysconfdir}/init.d/%{name}-fuse
%{_sysconfdir}/logrotate.d/%{name}-fuse
%{_sbindir}/%{name}-fuse
%{_datadir}/man1/argonaut-fuse.1.gz

%files fai-monitor
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
/usr/sbin/%{name}-fai-monitor
%{_datadir}/man1/%{name}-fai-monitor.1.gz
%{_sysconfdir}/init.d/%{name}-fai-monitor

%files yumgroup2yumi
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
/usr/sbin/yumgroup2yumi
%{_datadir}/man1/yumgroup2yumi.1.gz

%files dovecot
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
%{_datadir}/perl5/Argonaut/ClientDaemon/Modules/Dovecot.pm

%files server-module-fai
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
%{_datadir}/perl5/Argonaut/Server/Modules/FAI.pm

%files server-module-opsi
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
%{_datadir}/perl5/Argonaut/Server/Modules/OPSI.pm

%files common-fai
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
%{_datadir}/perl5/Argonaut/Libraries/FAI.pm


#date + "%a %b %d %Y"
%changelog
* Tue Sep 1 2015 SWAELENS Jonathan <jonathan@opensides.be> - 0.9.3-1
- Add many requires for argonaut-server and argonaut-common

* Fri Apr 26 2015 SWAELENS Jonathan <jonathan@opensides.be> - 0.9.2-1
- Add argonaut-fai-monitor package
- Add yumgroup2yumi package
- Remove argonaut-fai-mirror because it is only for Debian repository
- Add argonaut-server-module-opsi

* Thu Jul 10 2014 SWAELENS Jonathan <jonathan@opensides.be> - 0.9.1-1
- First upstream release in RPM
