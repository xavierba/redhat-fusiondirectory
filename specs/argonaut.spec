Name:		argonaut
Version:	VERSION_ARGONAUT	
Release:	BUILDNUMBER
Summary:	Tool to convert schema into ldif format

Group:		Applications/System
License:	BSD
URL:		https://forge.fusiondirectory.org/projects/argonaut

Source0:	%{name}-%{version}.tar.gz
Source1:        argonaut-client.init
Source2:        argonaut-fuse.init
Source3:        argonaut-server.init

Patch0:         argonaut-fix-ldap-directory.patch

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch
BuildRequires: 	wget

%description
Argonaut json rpc server to manage deployment system

%package client
Summary:        Argonaut json rpc server to manage deployment system
Requires:	argonaut-common, perl-Config-IniFiles, perl-Log-Handler, perl-File-Pid, perl-App-Daemon
Requires:	perl-JSON >= 2.07-1, perl-JSON-RPC, redhat-lsb-core
%description client
Argonaut client to manage computers and services.

%package common
Summary:        Argonaut common functions and librairies
Requires:	coreutils >= 6.10-1, openldap-clients
Requires:	perl-IO-Socket-SSL, perl-Path-Class, perl-LDAP
%description common
Common perl libraries used by the Argonaut deployment system.

%package common-fai
Summary:        Argonaut common library for FAI
Requires:	coreutils >= 6.10-1, argonaut-common, openldap-clients, perl-IO-Socket-SSL
Requires: 	perl-Net-LDAP-Server, perl-Path-Class
%description common-fai
Library for FAI (Fully Automated install) used by the Argonaut deployment system.

%package dovecot
Summary:        Argonaut client-module for dovecot
%description dovecot
Argonaut client module to manage the creation of the directory for the user where is mailbox is created.

%package fai-mirror
Summary:        Scripts to manage debian mirrors
Requires:	argonaut-common, perl-Net-LDAP-Server, perl-Log-Handler
Requires: 	perl-Config-IniFiles, debmirror
#Requires:       libwww-perl
%description fai-mirror
This package contains the tools to manage local mirror and external mirrors.

#%package fai-nfsroot
#Summary:        Tools, queues and status management
#Requires:	argonaut-common, argonaut-common-fai, fai-client >= 3.2.8, libconfig-inifiles-perl
#Requires:	libnet-ldap-perl, libjson-perl >= 2.07-1, libjson-rpc-perl, liblog-handler-perl
#Requires:	console-utilities, debootstrap
#%description fai-nfsroot
#Tools, queues and status management for FAI (Fully Automated Install) installations.

#%package fai-server
#Summary:        Scripts to enable Argonaut integration with FAI
#Requires:	argonaut-common, fai-client >= 3.2.8, fai-server >= 3.2.8, libnet-ldap-perl
#%description fai-server
#Programs, script and FAI nfsroot hooks to Integrate Argonaut into an FAI server nfsroot.

%package fuse
Summary:        Modular TFTP/Fuse supplicant
Requires:	argonaut-common, perl-Log-Handler, perl-Config-IniFiles, perl-Fuse
Requires:	perl-File-Pid, perl-Net-LDAP-Server, redhat-lsb-core
#Requires:      ucf, fuse-utils
%description fuse
Argonaut-fuse is a modular fuse-tftp-supplicant written in perl which allows
to create pxelinux configurations for different types of clients using external modules

%package fuse-module-fai
Summary:        LDAP FAI module for the TFTP/Fuse supplicant
Requires:      argonaut-fuse
%description fuse-module-fai
FAI module for argonaut-fuse which is using the LDAP backend in conjunction
with FusionDirectory and Argonaut to generate client configurations.

%package fuse-module-opsi
Summary:        LDAP FAI module for the TFTP/Fuse supplicant
Requires:      argonaut-fuse
%description fuse-module-opsi
FAI module for argonaut-fuse which is using the LDAP backend in conjunction
with FusionDirectory and Argonaut to generate client configurations.

%package ldap2zone
Summary:        Argonaut tool to extract DNS zones from LDAP trees
Requires:	argonaut-common, perl-Config-IniFiles, perl-Net-LDAP-Server, perl-DNS-ZoneParse >= 1.10
Conflicts:	ldap2zone
%description ldap2zone
This is a tool that reads info for a zone from LDAP and constructs
a standard plain ascii zone file. The LDAP information has to be
stored using the dnszone schema.

%package quota
Summary:        Argonaut tool to apply disk quota from ldap
Requires:	argonaut-common, perl-Config-IniFiles, perl-Net-LDAP-Server, perl-Quota, quota
%description quota
This is a tool that reads info for quota from LDAP and apply it
to your quota server. The LDAP information has to be stored using
the fdQuota schema.

%package server
Summary:        Argonaut json rpc server to manage deployment system
Requires:	argonaut-common
Requires:	perl-DateTime, perl-LDAP, perl-Log-Handler, perl-POE-Component-Schedule
Requires:	perl-POE-Component-Server-SimpleHTTP
Requires:	perl-POE-Component-Pool-Thread, perl-POE-Component-Server-JSONRPC
Requires:	perl-JSON-RPC, perl-File-Pid, perl-App-Daemon,  perl-JSON >= 2.07-1
Requires:	perl-Config-IniFiles, perl-POE, redhat-lsb-core
%description server
Argonaut server to manage deployment systems.

%package server-module-fai
Summary:        Argonaut json rpc server module to manage FAI (Fully Automated Install)
Requires:	argonaut-server
%description server-module-fai
Argonaut server module to manage FAI (Fully Automated Install) installation.

%prep
%setup -q -n %{name}-%{version}
%patch0

# Download default script
####wget http://git.fusiondirectory.org/code/packaging/debian.git/plain/argonaut/argonaut-client.default?h=argonaut-0.9.1
####wget http://git.fusiondirectory.org/code/packaging/debian.git/plain/argonaut/argonaut-server.default?h=argonaut-0.9.1


# Manpages in gz
gzip ./argonaut-server/man/argonaut-server.1
gzip ./argonaut-client/man/argonaut-client.1
gzip ./argonaut-ldap2zone/man/argonaut-ldap2zone.1
gzip ./argonaut-quota/man/argonaut-quota.1
gzip ./argonaut-fai-mirror/man/argonaut-repository.1
gzip ./argonaut-fai-nfsroot/man/ldap2fai.1
gzip ./argonaut-fuse/man/argonaut-fuse.1

%build

%install
# Clean buildroot before install
rm -rf %{buildroot} 

# Directories
mkdir -p %{buildroot}/%{_sbindir}/
mkdir -p %{buildroot}/%{_datadir}/perl5/
mkdir -p %{buildroot}/%{_datadir}/man1/
mkdir -p %{buildroot}/%{_sysconfdir}/argonaut/
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

# Copy default files
####cp ./%{name}-client.default?h=%{name}-%{version} %{buildroot}/%{_sysconfdir}/default/%{name}-client
####cp ./%{name}-server.default?h=%{name}-%{version} %{buildroot}/%{_sysconfdir}/default/%{name}-server

# Install argonaut-server-module-fai
cd ./argonaut-server
cp ./Argonaut/Server/Modules/FAI.pm %{buildroot}/%{_datadir}/perl5/Argonaut/Server/Modules/

# Install argonaut-server
cp ./bin/* %{buildroot}/%{_sbindir}/
cp -a ./Argonaut/ %{buildroot}/%{_datadir}/perl5/
cp ./man/argonaut-server.1.gz %{buildroot}/%{_datadir}/man1/
cd ..

# Install argonaut-client
cd ./argonaut-client
cp ./bin/* %{buildroot}/%{_sbindir}/
cp ./Argonaut/ClientDaemon.pm %{buildroot}/%{_datadir}/perl5/Argonaut/
cp ./Argonaut/ClientDaemon/Modules/Service.pm %{buildroot}/%{_datadir}/perl5/Argonaut/ClientDaemon/Modules/
cp ./Argonaut/ClientDaemon/Modules/System.pm  %{buildroot}/%{_datadir}/perl5/Argonaut/ClientDaemon/Modules/
cp ./man/argonaut-client.1.gz %{buildroot}/%{_datadir}/man1/
cd ..

# Install argonaut-common
cd ./argonaut-common
cp ./Argonaut/Libraries/Common.pm  %{buildroot}/%{_datadir}/perl5/Argonaut/Libraries/
cp ./Argonaut/Libraries/Packages.pm %{buildroot}/%{_datadir}/perl5/Argonaut/Libraries/
cp ./argonaut.conf %{buildroot}/%{_sysconfdir}/argonaut/

# Install argonaut-common-fai
cp ./Argonaut/Libraries/FAI.pm %{buildroot}/%{_datadir}/perl5/Argonaut/Libraries/
cd ..

# Install argonaut-dovecot
cd ./argonaut-dovecot
cp ./Argonaut/ClientDaemon/Modules/Dovecot.pm %{buildroot}/%{_datadir}/perl5/Argonaut/ClientDaemon/Modules/
cd ..

# Install argonaut-fai-mirror
cd ./argonaut-fai-mirror
cp ./bin/* %{buildroot}/%{_sbindir}/
cp ./man/argonaut-repository.1.gz %{buildroot}/%{_datadir}/man1/
cd ..

# Install argonaut-fai-nfsroot
#cd ./argonaut-fai-nfsroot
#cp ./bin/* %{buildroot}/%{_sbindir}/
#cp ./lib/get-config-dir-argonaut %{buildroot}/usr/lib/fai/
#cp ./man/ldap2fai.1.gz %{buildroot}/%{_datadir}/man1/
#cd ..

# Install argonaut-fai-server
#cd ./argonaut-fai-server
#cp ./nfsroot-hooks/argonaut-nfsroot-integration %{buildroot}/%{_sysconfdir}/fai/nfsroot-hooks/
#cp ./bin/* %{buildroot}/%{_sbindir}/
#cd .. 

# Install argonaut-fuse-module-fai
cd ./argonaut-fuse
cp ./Argonaut/Fuse/Modules/FAI.pm  %{buildroot}/%{_datadir}/perl5/Argonaut/Fuse/Modules/

# Install argonaut-fuse-module-opsi
cp ./Argonaut/Fuse/Modules/OPSI.pm  %{buildroot}/%{_datadir}/perl5/Argonaut/Fuse/Modules/

# Install argonaut-fuse
cp ./bin/argonaut-fuse %{buildroot}/%{_sbindir}/
cp ./man/argonaut-fuse.1.gz %{buildroot}/%{_datadir}/man1/

# Logrotate config
mkdir -p %{buildroot}/etc/logrotate.d/
#####wget 'http://git.fusiondirectory.org/code/packaging/debian.git/plain/argonaut/argonaut-fuse.logrotate?h=argonaut-0.9.1'
####cp argonaut-fuse.logrotate* %{buildroot}/etc/logrotate.d/%{name}-fuse
cd ..

# Install argonaut-ldap2zone
cd ./argonaut-ldap2zone
cp ./bin/* %{buildroot}/%{_sbindir}/
cp -a ./Argonaut/ %{buildroot}/%{_datadir}/perl5/
cp ./man/argonaut-ldap2zone.1.gz %{buildroot}/%{_datadir}/man1/
cd ..

# Install argonaut-quota
cd ./argonaut-quota
cp ./bin/* %{buildroot}/%{_sbindir}/
cp -a ./Argonaut/ %{buildroot}/%{_datadir}/perl5/
cp ./man/argonaut-quota.1.gz %{buildroot}/%{_datadir}/man1/
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
####/etc/default/%{name}-client
%{_sbindir}/argonaut-client
%{_datadir}/perl5/Argonaut/ClientDaemon.pm 
%{_datadir}/perl5/Argonaut/ClientDaemon/Modules/Service.pm
%{_datadir}/perl5/Argonaut/ClientDaemon/Modules/System.pm
%{_datadir}/man1/argonaut-client.1.gz

%files common
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
%{_sysconfdir}/argonaut/argonaut.conf
%{_datadir}/perl5/Argonaut/Libraries/Common.pm
%{_datadir}/perl5/Argonaut/Libraries/Packages.pm 

%files ldap2zone
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
%{_sbindir}/argonaut-ldap2zone
%{_datadir}/perl5/Argonaut/Libraries/Ldap2zone.pm 
%{_datadir}/perl5/Argonaut/ClientDaemon/Modules/Ldap2Zone.pm
%{_datadir}/man1/argonaut-ldap2zone.1.gz

%files quota
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
%{_sbindir}/argonaut-quota
%{_datadir}/perl5/Argonaut/Libraries/Quota.pm
%{_datadir}/man1/argonaut-quota.1.gz

%files server
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
/etc/init.d/%{name}-server
####/etc/default/%{name}-server
%{_sbindir}/argonaut-server
%{_datadir}/perl5/Argonaut/Server/ModulesPool.pm
%{_datadir}/perl5/Argonaut/Server/Modules/Argonaut.pm

%{_datadir}/perl5/Argonaut/Server/Modules/OPSI.pm

%{_datadir}/man1/argonaut-server.1.gz

%files fuse-module-fai
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
%{_datadir}/man1/argonaut-fuse.1.gz
%{_datadir}/perl5/Argonaut/Fuse/Modules/FAI.pm

%files fuse-module-opsi
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
%{_datadir}/man1/argonaut-fuse.1.gz
%{_datadir}/perl5/Argonaut/Fuse/Modules/OPSI.pm

%files fuse
%defattr(-,root,root,-)
%doc README AUTHORS Changelog
%{_sysconfdir}/init.d/%{name}-fuse
####/etc/logrotate.d/%{name}-fuse
%{_sbindir}/argonaut-fuse
%{_datadir}/man1/argonaut-fuse.1.gz

#%files fai-server
#/etc/fai/nfsroot-hooks/argonaut-nfsroot-integration
#/usr/sbin/fai2ldif
#/usr/sbin/argonaut-fai-monitor

#%files fai-nfsroot
#/usr/sbin/ldap2fai
#/usr/lib/fai/get-config-dir-argonaut
#/usr/share/man1/ldap2fai.1.gz

%files fai-mirror
/usr/sbin/argonaut-repository
/usr/sbin/argonaut-debconf-crawler
%{_datadir}/man1/argonaut-repository.1.gz

%files dovecot
%{_datadir}/perl5/Argonaut/ClientDaemon/Modules/Dovecot.pm

%files server-module-fai
%{_datadir}/perl5/Argonaut/Server/Modules/FAI.pm

%files common-fai
%{_datadir}/perl5/Argonaut/Libraries/FAI.pm

%changelog

