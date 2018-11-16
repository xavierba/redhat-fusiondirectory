# This is the header.spec file
Name:       fusiondirectory-plugin
Version:    _VERSION_
Release:    _RELEASE_
Summary:    Web Based LDAP Administration Program

Group:      Applications/System
License:    GPLv2
URL:        http://www.fusiondirectory.org

Buildarch:  noarch
Source0:    fusiondirectory-%{version}.tar.gz
Source1:    fusiondirectory-plugins-%{version}.tar.gz

Requires:   php54-common, php54-ldap, php54-imap, php54-mbstring, php54-pecl-imagick, php54-fpdf
Requires:   httpd, gettext, openldap-servers, openldap-clients, perl-ExtUtils-MakeMaker
Requires:   prototype, prototype-httpd, scriptaculous, scriptaculous-httpd
Requires:   php54-php-Smarty3, php54-php-Smarty3-i18n, schema2ldif

%description
FusionDirectory is a combination of system-administrator and end-user web
interface, designed to handle LDAP based setups.
Provided is access to posix, shadow, samba, proxy, and Kerberos
accounts. It is able to manage the Postfix/Cyrus server combination
and can write user adapted sieve scripts.


# This is the prep.spec file
%prep

# Create build directory
%setup -c -q -n fusiondirectory-%{version}

# Source FD-core
# Extract Source
%setup -T -D -b 0 -n fusiondirectory-%{version}

# Builroot
cd ..

# Extract Source 1
%setup -T -D -b 1 -n fusiondirectory-plugins-%{version}

# This is the install.spec file
%install
rm -Rf %{buildroot}

# Builroot
cd ..

#Installation of FD-plugins
# Core plugins installation
PLUGINS_LIST=`find fusiondirectory-plugins-%{version}/ -mindepth 1 -maxdepth 1 -type d ! -name heimdal -a ! -name mit-krb5 -a ! -name log -a ! -name .tx`

# Entering plugins topdir
cd fusiondirectory-plugins-%{version}/

for cur_plugin_line in ${PLUGINS_LIST} ; do
  # Entering Plugins Directory
  cur_plugin=$(basename ${cur_plugin_line})
  cd ${cur_plugin}


  # Plugin developers
  if [ "${cur_plugin}" = "developers" ] ; then
    mkdir -p %{buildroot}%{_datadir}/doc/fusiondirectory-developers/
    mkdir -p %{buildroot}%{_datadir}/fusiondirectory/plugins/addons
    cp -a ./debug-help/addons/. %{buildroot}%{_datadir}/fusiondirectory/plugins/addons/

  else

    # First folders going to %{buildroot}%{_datadir}/fusiondirectory/plugins/

    # Addons section
    if [ -d ./addons ] ; then
      mkdir -p %{buildroot}%{_datadir}/fusiondirectory/plugins/addons/
      cp -a ./addons/. %{buildroot}%{_datadir}/fusiondirectory/plugins/addons/
    fi

    # Admin section
    if [ -d ./admin ] ; then
      mkdir -p %{buildroot}%{_datadir}/fusiondirectory/plugins/admin/
      cp -a ./admin/. %{buildroot}%{_datadir}/fusiondirectory/plugins/admin/
    fi

    # Config section
    if [ -d ./config ] ; then
      mkdir -p %{buildroot}%{_datadir}/fusiondirectory/plugins/config/
      cp -a ./config/. %{buildroot}%{_datadir}/fusiondirectory/plugins/config/
    fi

    # Personal section
    if [ -d ./personal ] ; then
      mkdir -p %{buildroot}%{_datadir}/fusiondirectory/plugins/personal/
      cp -a ./personal/. %{buildroot}%{_datadir}/fusiondirectory/plugins/personal/
    fi

    # Then folders going to %{buildroot}%{_datadir}/fusiondirectory/

    # HTML section
    if [ -d ./html ] ; then
      mkdir -p %{buildroot}%{_datadir}/fusiondirectory/html/
      cp -a ./html/. %{buildroot}%{_datadir}/fusiondirectory/html/
    fi

    # IHTML section
    if [ -d ./ihtml ] ; then
      mkdir -p %{buildroot}%{_datadir}/fusiondirectory/ihtml/
      cp -a ./ihtml/. %{buildroot}%{_datadir}/fusiondirectory/ihtml/
    fi

    # Include section
    if [ -d ./include ] ; then
      mkdir -p %{buildroot}%{_datadir}/fusiondirectory/include/
      cp -a ./include/. %{buildroot}%{_datadir}/fusiondirectory/include/
    fi

    # Locale section
    if [ -d ./locale ] ; then
      mkdir -p %{buildroot}%{_datadir}/fusiondirectory/locale/plugins/${cur_plugin}/locale/
      cp -a ./locale/. %{buildroot}%{_datadir}/fusiondirectory/locale/plugins/${cur_plugin}/locale/
    fi

    # Contrib sections

    # Openldap section
    if [ -d ./contrib/openldap ] ; then
      mkdir -p %{buildroot}%{_sysconfdir}/openldap/schema/fusiondirectory/
      cp -a ./contrib/openldap/. %{buildroot}%{_sysconfdir}/openldap/schema/fusiondirectory/

      mkdir -p %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-${cur_plugin}-schema/
      cp ../../fusiondirectory-%{version}/{AUTHORS.md,Changelog,LICENSE} %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-${cur_plugin}-schema/
    fi

    # Docs section
    if [ -d ./contrib/docs ] ; then
      mkdir -p %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-${cur_plugin}/
      cp -a ./contrib/docs/. %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-${cur_plugin}/
    fi

    # Etc section
    if [ -d ./contrib/etc ] ; then
      mkdir -p %{buildroot}%{_sysconfdir}/fusiondirectory/${cur_plugin}/
      cp -a ./contrib/etc/. %{buildroot}%{_sysconfdir}/fusiondirectory/supann/
    fi
  fi

  # Docs
  mkdir -p %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-${cur_plugin}/
  cp ../../fusiondirectory-%{version}/{AUTHORS.md,Changelog,LICENSE} %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-${cur_plugin}/

  # Exiting plugin directory
  cd ..
done


%clean
rm -Rf %{buildroot}


%package alias
Group:          Applications/System
Summary:        Manage fonctional aliases
Requires:       fusiondirectory >= %{version},fusiondirectory-plugin-mail

%description alias
Manage fonctional aliases

%package argonaut
Group:          Applications/System
Summary:        Communication layer between various software and the JSON-RPC Argonaut Server
Requires:       fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description argonaut
Communication layer between various software and the JSON-RPC Argonaut Server

%package autofs
Group:          Applications/System
Summary:        Management of automount entries
Requires:       fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description autofs
Management of automount entries

%package cyrus
Group:    Applications/System
Summary:  Cyrus account management
Requires: fusiondirectory >= %{version}, fusiondirectory-plugin-systems >= %{version}

%description cyrus
Cyrus account management

%package debconf
Group:    Applications/System
Summary:  Management of debconf profile
Requires: fusiondirectory >= %{version},fusiondirectory-plugin-argonaut

%description debconf
Management of debconf profile

%package developers
Group:    Applications/System
Summary:  Management plugin for developers
Requires: fusiondirectory >= %{version}

%description developers
Management plugin for developers

%package dhcp
Group:    Applications/System
Summary:  DHCP service management
Requires: fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description dhcp
DHCP service management

%package dns
Group:    Applications/System
Summary:  DNS service management
Requires: fusiondirectory >= %{version}

%description dns
DNS service management

%package dovecot
Group:    Applications/System
Summary:  Dovecot account management
Requires: fusiondirectory >= %{version}, fusiondirectory-plugin-systems >= %{version}

%description dovecot
Dovecot account management

%package dsa
Group:    Applications/System
Summary:  Manage service security account in the LDAP
Requires: fusiondirectory >= %{version}

%description dsa
Manage service security account in the LDAP

%package fai
Group:    Applications/System
Summary:  Linux system deployment management
Requires: fusiondirectory >= %{version},fusiondirectory-plugin-systems,fusiondirectory-plugin-argonaut

%description fai
Linux system deployment management

%package freeradius
Group:    Applications/System
Summary:  Manage users and groups for a freeradius server
Requires: fusiondirectory >= %{version}

%description freeradius
Manage users and groups for a freeradius server

%package fusioninventory
Group:    Applications/System
Summary:  Fusioninventory inventory Management
Requires: fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description fusioninventory
Fusioninventory inventory Management

%package gpg
Group:    Applications/System
Summary:  Management plugin for gpg
Requires: fusiondirectory >= %{version}

%description gpg
Management plugin for gpg

%package ipmi
Group:    Applications/System
Summary:  Basic ipmi support
Requires: fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description ipmi
Basic ipmi support

%package ldapdump
Group:    Applications/System
Summary:  Ldap raw visualisation
Requires: fusiondirectory >= %{version}

%description ldapdump
Ldap raw visualisation

%package ldapmanager
Group:    Applications/System
Summary:  Simple LDAP backup and insertion tasks
Requires: fusiondirectory >= %{version},openldap-clients

%description ldapmanager
Simple LDAP backup and insertion tasks

%package mail
Group:    Applications/System
Summary:  Mail management base
Requires: fusiondirectory >= %{version}

%description mail
Mail management base

%package nagios
Group:    Applications/System
Summary:  Nagios account settings management
Requires: fusiondirectory >= %{version}

%description nagios
Nagios account settings management

%package netgroups
Group:    Applications/System
Summary:  Nis Netgroups account management
Requires: fusiondirectory >= %{version}

%description netgroups
Nis Netgroups account management

%package opsi
Group:    Applications/System
Summary:  Opsi deployment management for Windows clients
Requires: fusiondirectory >= %{version},fusiondirectory-plugin-systems,fusiondirectory-plugin-dns,fusiondirectory-plugin-samba

%description opsi
Opsi deployment management for Windows clients

%package puppet
Group:    Applications/System
Summary:  Manage a puppet server
Requires: fusiondirectory >= %{version}

%description puppet
Manage a puppet server

%package pureftpd
Group:    Applications/System
Summary:  PureFTPD connectivity plugin
Requires: fusiondirectory >= %{version}

%description pureftpd
PureFTPD connectivity plugin

%package quota
Group:    Applications/System
Summary:  Plugin for storing filesystem quota per user inside LDAP tree
Requires: fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description quota
Plugin for storing filesystem quota per user inside LDAP tree

%package repository
Group:    Applications/System
Summary:  Plugin to manage repository for build systems
Requires: fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description repository
Plugin to manage repository for build systems

%package samba
Group:    Applications/System
Summary:  Samba 3 integration
Requires: fusiondirectory >= %{version},fusiondirectory-plugin-systems,fusiondirectory-plugin-posix >= %{version}

%description samba
Samba 3 integration

%package sogo
Group:    Applications/System
Summary:  SOgo Account Management
Requires: fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description sogo
SOgo Account Management

%package squid
Group:    Applications/System
Summary:  Squid connectivity plugin
Requires: fusiondirectory >= %{version}

%description squid
Squid connectivity plugin

%package ssh
Group:    Applications/System
Summary:  SSH key plugin
Requires: fusiondirectory >= %{version}, fusiondirectory-plugin-posix >= %{version}

%description ssh
SSH key plugin

%package sudo
Group:    Applications/System
Summary:  Sudo manager
Requires: fusiondirectory >= %{version}, fusiondirectory-plugin-systems >= %{version}

%description sudo
Sudo manager

%package supann
Group:    Applications/System
Summary:  This Plugin aims to provide a full LDAP interface to SUPANN schema
Requires: fusiondirectory >= %{version}

%description supann
This Plugin aims to provide a full LDAP interface to SUPANN schema

%package sympa
Group:    Applications/System
Summary:  Management of alias list of sympa
Requires: fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description sympa
Management of alias list of sympa

%package systems
Group:    Applications/System
Summary:  System management base plugin
Requires: fusiondirectory >= %{version}

%description systems
System management base plugin

%package weblink
Group:    Applications/System
Summary:  Plugin to access remote management of systems
Requires: fusiondirectory >= %{version}, fusiondirectory-plugin-systems >= %{version}

%description weblink
Plugin to access remote management of systems

%package webservice
Group:    Applications/System
Summary:  Management plugin for webservice
Requires: fusiondirectory >= %{version}

%description webservice
Management plugin for webservice

%package ejbca
Group:          Applications/System
Summary:        Management plugin for ejbca
Requires:       fusiondirectory >= %{version}

%description ejbca
Management plugin for ejbca

%package applications
Group:          Applications/System
Summary:        Management plugin for applications
Requires:       fusiondirectory >= %{version}

%description applications
Management plugin for applications

%package personal
Group:          Applications/System
Summary:        Management plugin for personal
Requires:       fusiondirectory >= %{version}

%description personal
Management plugin for personal

%package ppolicy
Group:          Applications/System
Summary:        Management plugin for personal
Requires:       fusiondirectory >= %{version}

%description ppolicy
Management plugin for ppolicy

%package certificates
Group:          Applications/System
Summary:        Management plugin for certificates
Requires:       fusiondirectory >= %{version}

%description certificates
Management plugin for certificates

%package mixedgroups
Group:          Applications/System
Summary:        Management plugin for mixedgroups
Requires:       fusiondirectory >= %{version}

%description mixedgroups
Management plugin for mixedgroups

%package subcontracting
Group:          Applications/System
Summary:        Management plugin for subcontracting
Requires:       fusiondirectory >= %{version}

%description subcontracting
Management plugin for subcontracting

%package newsletter
Group:          Applications/System
Summary:        Management plugin for newsletter
Requires:       fusiondirectory >= %{version}

%description newsletter
Management plugin for newsletter

%package community
Group:          Applications/System
Summary:        Management plugin for community
Requires:       fusiondirectory >= %{version}

%description community
Management plugin for community

%package postfix
Group:          Applications/System
Summary:        Management plugin for postfix
Requires:       fusiondirectory >= %{version}, fusiondirectory-plugin-systems >= %{version}

%description postfix
Management plugin for postfix

%package spamassassin
Group:          Applications/System
Summary:        Management plugin for spamassassin
Requires:       fusiondirectory >= %{version}, fusiondirectory-plugin-systems >= %{version}

%description spamassassin
Management plugin for spamassassin

%package user-reminder
Group:          Applications/System
Summary:        Management plugin for user-reminder
Requires:       fusiondirectory >= %{version}

%description user-reminder
Management plugin for user-reminder

%package audit
Group:          Applications/System
Summary:        Management plugin for audit
Requires:       fusiondirectory >= %{version}

%description audit
Management plugin for audit

%package renater-partage
Group:          Applications/System
Summary:        Management plugin for renater-partage
Requires:       fusiondirectory >= %{version}

%description renater-partage
Management plugin for renater-partage

%package posix
Group:          Applications/System
Summary:        Management plugin for posix
Requires:       fusiondirectory >= %{version}

%description posix
Management plugin for posix


%package alias-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory alias plugin
Requires: fusiondirectory-plugin-mail-schema >= %{version}

%description alias-schema
LDAP schema for FusionDirectory alias plugin

%package argonaut-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory argonaut plugin
Requires: fusiondirectory-plugin-systems-schema >= %{version}

%description argonaut-schema
LDAP schema for FusionDirectory argonaut plugin



%package autofs-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory autofs plugin
Requires: fusiondirectory-plugin-systems-schema >= %{version}

%description autofs-schema
LDAP schema for FusionDirectory autofs plugin



%package cyrus-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory cyrus plugin
Requires: fusiondirectory-schema >= %{version}, fusiondirectory-plugin-systems-schema >= %{version}

%description cyrus-schema
LDAP schema for FusionDirectory cyrus plugin



%package debconf-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory debconf plugin
Requires: fusiondirectory-plugin-argonaut-schema >= %{version}

%description debconf-schema
LDAP schema for FusionDirectory debconf plugin



%package dhcp-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory dhcp plugin
Requires: fusiondirectory-plugin-systems-schema >= %{version}

%description dhcp-schema
LDAP schema for FusionDirectory dhcp plugin



%package dns-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory dns plugin

%description dns-schema
LDAP schema for FusionDirectory dns plugin



%package dovecot-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory dovecot plugin
Requires: fusiondirectory-schema >= %{version}, fusiondirectory-plugin-systems-schema >= %{version}

%description dovecot-schema
LDAP schema for FusionDirectory dovecot plugin



%package dsa-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory dsa plugin
Requires: fusiondirectory-schema >= %{version}

%description dsa-schema
LDAP schema for FusionDirectory dsa plugin



%package fai-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory fai plugin
Requires: fusiondirectory-plugin-systems-schema >= %{version}, fusiondirectory-plugin-argonaut-schema >= %{version}

%description fai-schema
LDAP schema for FusionDirectory fai plugin



%package freeradius-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory freeradius plugin
Requires: fusiondirectory-schema >= %{version}

%description freeradius-schema
LDAP schema for FusionDirectory freeradius plugin



%package fusioninventory-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory fusioninventory plugin
Requires: fusiondirectory-plugin-systems-schema >= %{version}

%description fusioninventory-schema
LDAP schema for FusionDirectory fusioninventory plugin



%package gpg-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory gpg plugin
Requires: fusiondirectory-plugin-systems-schema >= %{version}

%description gpg-schema
LDAP schema for FusionDirectory gpg plugin



%package ipmi-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory ipmi plugin
Requires: fusiondirectory-plugin-systems-schema >= %{version}

%description ipmi-schema
LDAP schema for FusionDirectory ipmi plugin



%package mail-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory mail plugin
Requires: fusiondirectory-schema >= %{version}

%description mail-schema
LDAP schema for FusionDirectory mail plugin



%package nagios-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory nagios plugin
Requires: fusiondirectory-schema >= %{version}

%description nagios-schema
LDAP schema for FusionDirectory nagios plugin



%package netgroups-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory netgroups plugin
Requires: fusiondirectory-schema >= %{version}

%description netgroups-schema
LDAP schema for FusionDirectory netgroups plugin



%package opsi-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory opsi plugin
Requires: fusiondirectory-plugin-systems-schema >= %{version}, fusiondirectory-plugin-dns-schema >= %{version}, fusiondirectory-plugin-samba-schema >= %{version}

%description opsi-schema
LDAP schema for FusionDirectory opsi plugin



%package puppet-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory puppet plugin
Requires: fusiondirectory-schema >= %{version}

%description puppet-schema
LDAP schema for FusionDirectory puppet plugin



%package pureftpd-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory pureftpd plugin
Requires: fusiondirectory-schema >= %{version}

%description pureftpd-schema
LDAP schema for FusionDirectory pureftpd plugin



%package quota-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory quota plugin
Requires: fusiondirectory-plugin-systems-schema >= %{version}

%description quota-schema
LDAP schema for FusionDirectory quota plugin



%package repository-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory repository plugin
Requires: fusiondirectory-plugin-systems-schema >= %{version}

%description repository-schema
LDAP schema for FusionDirectory repository plugin



%package samba-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory samba plugin
Requires: fusiondirectory-plugin-systems-schema >= %{version}

%description samba-schema
LDAP schema for FusionDirectory samba plugin



%package sogo-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory sogo plugin
Requires: fusiondirectory-plugin-systems-schema >= %{version}

%description sogo-schema
LDAP schema for FusionDirectory sogo plugin



%package squid-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory squid plugin
Requires: fusiondirectory-schema >= %{version}

%description squid-schema
LDAP schema for FusionDirectory squid plugin



%package ssh-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory ssh plugin
Requires: fusiondirectory-schema >= %{version}

%description ssh-schema
LDAP schema for FusionDirectory ssh plugin



%package sudo-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory sudo plugin
Requires:   fusiondirectory-schema >= %{version}, fusiondirectory-plugin-systems-schema >= %{version}

%description sudo-schema
LDAP schema for FusionDirectory sudo plugin



%package supann-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory supann plugin
Requires: fusiondirectory-schema >= %{version}

%description supann-schema
LDAP schema for FusionDirectory supann plugin



%package sympa-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory sympa plugin
Requires: fusiondirectory-plugin-systems-schema >= %{version}

%description sympa-schema
LDAP schema for FusionDirectory sympa plugin



%package systems-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory systems plugin
Requires: fusiondirectory-schema >= %{version}

%description systems-schema
LDAP schema for FusionDirectory systems plugin



%package weblink-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory weblink plugin
Requires: fusiondirectory-plugin-systems-schema >= %{version}

%description weblink-schema
LDAP schema for FusionDirectory weblink plugin



%package webservice-schema
Group:    Applications/System
Summary:  LDAP schema for FusionDirectory webservice plugin
Requires: fusiondirectory-schema >= %{version}

%description webservice-schema
LDAP schema for FusionDirectory webservice plugin

%package ejbca-schema
Group:          Applications/System
Summary:        LDAP schema for FusionDirectory ejbca plugin

%description ejbca-schema
LDAP schema for FusionDirectory ejbca plugin

%package applications-schema
Group:          Applications/System
Summary:        LDAP schema for FusionDirectory applications plugin

%description applications-schema
LDAP schema for FusionDirectory applications plugin

%package personal-schema
Group:          Applications/System
Summary:        LDAP schema for FusionDirectory personal plugin

%description personal-schema
LDAP schema for FusionDirectory personal plugin

%package ppolicy-schema
Group:          Applications/System
Summary:        LDAP schema for FusionDirectory ppolicy plugin

%description ppolicy-schema
LDAP schema for FusionDirectory ppolicy plugin

%package subcontracting-schema
Group:          Applications/System
Summary:        LDAP schema for FusionDirectory subcontracting plugin

%description subcontracting-schema
LDAP schema for FusionDirectory subcontracting plugin

%package newsletter-schema
Group:          Applications/System
Summary:        LDAP schema for FusionDirectory newsletter plugin

%description newsletter-schema
LDAP schema for FusionDirectory newsletter plugin

%package community-schema
Group:          Applications/System
Summary:        LDAP schema for FusionDirectory community plugin

%description community-schema
LDAP schema for FusionDirectory community plugin

%package postfix-schema
Group:          Applications/System
Summary:        LDAP schema for FusionDirectory postfix plugin
Requires:       fusiondirectory-schema >= %{version}, fusiondirectory-plugin-systems-schema >= %{version}

%description postfix-schema
LDAP schema for FusionDirectory postfix plugin

%package spamassassin-schema
Group:          Applications/System
Summary:        LDAP schema for FusionDirectory spamassassin plugin
Requires:       fusiondirectory-schema >= %{version}, fusiondirectory-plugin-systems-schema >= %{version}

%description spamassassin-schema
LDAP schema for FusionDirectory spamassassin plugin

%package user-reminder-schema
Group:          Applications/System
Summary:        LDAP schema for FusionDirectory user-reminder plugin
Requires:       fusiondirectory-schema >= %{version}

%description user-reminder-schema
LDAP schema for FusionDirectory user-reminder plugin

%package audit-schema
Group:          Applications/System
Summary:        LDAP schema for FusionDirectory audit plugin
Requires:       fusiondirectory-schema >= %{version}

%description audit-schema
LDAP schema for FusionDirectory audit plugin

%package renater-partage-schema
Group:          Applications/System
Summary:        LDAP schema for FusionDirectory renater-partage plugin
Requires:       fusiondirectory-schema >= %{version}

%description renater-partage-schema
LDAP schema for FusionDirectory renater-partage plugin


# Generated by script generate_post_plugins.sh
# This is the post_plugins.spec file
%post alias
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post argonaut
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post autofs
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post cyrus
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post debconf
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post developers
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post dhcp
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post dns
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post dovecot
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post dsa
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post fai
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post freeradius
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post fusioninventory
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post gpg
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post ipmi
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post ldapdump
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post ldapmanager
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post mail
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post nagios
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post netgroups
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post opsi
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post puppet
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post pureftpd
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post quota
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post repository
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post samba
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post sogo
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post squid
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post ssh
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post sudo
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post supann
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post sympa
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post systems
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post weblink
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post webservice
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%post ejbca
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%post personal
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%post ppolicy
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%post certificates
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%post mixedgroups
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%post applications
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%post subcontracting
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%post newsletter
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%post community
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%post postfix
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%post spamassassin
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%post user-reminder
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%post audit
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%post renater-partage
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%post posix
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


# Generated by script generate_postun_plugins.sh
# This is the postun_plugins.spec file
%postun alias
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun argonaut
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun autofs
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun cyrus
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun debconf
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun developers
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun dhcp
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun dns
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun dovecot
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun dsa
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun fai
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun freeradius
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun fusioninventory
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun gpg
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun ipmi
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun ldapdump
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun ldapmanager
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun mail
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun nagios
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun netgroups
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun opsi
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun puppet
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun pureftpd
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun quota
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun repository
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun samba
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun sogo
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun squid
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun ssh
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun sudo
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun supann
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun sympa
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun systems
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun weblink
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun webservice
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%postun applications
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%postun ejbca
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%postun personal
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%postun ppolicy
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%postun certificates
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%postun mixedgroups
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%postun subcontracting
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%postun newsletter
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%postun community
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%postun postfix
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%postun spamassassin
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%postun user-reminder
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%postun audit
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%postun renater-partage
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%postun posix
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%files alias
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/alias/class_aliasManagement.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/alias/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/alias/class_mailAliasDistribution.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/alias/class_mailAliasRedirection.inc
# Config section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/alias/class_aliasConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/alias-distribution.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/alias-redirection.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/alias-sympa.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/alias.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/alias.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/alias-distribution.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/alias-redirection.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/alias-sympa.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/alias.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/alias.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/alias
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-alias/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-alias/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-alias/LICENSE


%files argonaut
%defattr(0644,root,root,755)
# Addons section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/argonaut/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/argonaut/deploy-list.tpl
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/argonaut/class_argonautQueue.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/argonaut/class_filterArgonautEvents.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/argonaut/class_argonautImportFile.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/argonaut/class_argonautEventTypes.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/addons/argonaut/class_argonautAction.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/addons/argonaut/import_events.tpl
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/argonaut/deploy-list.xml
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/argonaut/deploy-filter.xml
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/argonaut/class_argonautDNSConfig.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/argonaut/class_argonautFuseConfig.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/argonaut/class_argonautMirrorConfig.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/argonaut/class_argonautFuseOPSIConfig.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/argonaut/class_argonautServer.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/argonaut/class_argonautFuseLTSPConfig.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/argonaut/class_argonautFuseFAIConfig.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/argonaut/class_argonautClient.inc
# HTML section
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/argonaut-dns.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/argonaut-fuse.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/argonaut-mirror.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/argonaut.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/argonaut.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/argonaut-dns.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/argonaut-fuse.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/argonaut-mirror.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/argonaut.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/argonaut.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/getFAIstatus.php
# Include section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/include/jsonRPCClient.php
%attr (-,root,root) %{_datadir}/fusiondirectory/include/class_supportDaemon.inc
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/argonaut
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-argonaut/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-argonaut/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-argonaut/LICENSE


%files autofs
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/autofs/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/autofs/class_nisMap.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/autofs/class_nisObject.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/autofs/class_autofsManagement.inc
# Config section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/autofs/class_autofsConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/autofs-nis-netmap.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/autofs-nis-object.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/autofs.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/autofs.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/autofs-nis-map.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/autofs-nis-object.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/autofs.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/autofs.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/autofs
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-autofs/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-autofs/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-autofs/LICENSE


%files cyrus
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/cyrus/class_serviceCyrus.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/cyrus.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/cyrus.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/cyrus.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/cyrus
# Files
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/personal/mail/mail-methods/sieve_script.tpl
# Personal section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/mail/mail-methods/class_mail-methods-cyrus.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-cyrus/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-cyrus/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-cyrus/LICENSE


%files debconf
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/debconf/class_debconfStartup.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/debconfProfile/debconfProfile-filter.tpl
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/debconfProfile/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/debconfProfile/class_debconfProfileManagement.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/debconfProfile/debconfProfile-filter.xml
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/debconfProfile/class_debconfProfileGeneric.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/debconf.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/debconf.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/debconf.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/debconf.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/debconf
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-debconf/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-debconf/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-debconf/LICENSE


%files developers
%defattr(0644,root,root,755)
%attr (-,root,root) %{_datadir}/doc/fusiondirectory-developers/
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/debug-help
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-developers/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-developers/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-developers/LICENSE


%files dhcp
%defattr(0644,root,root,755)
# HTML section
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/dhcp.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/dhcp.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/dhcp.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/dhcp.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/dhcp/
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/dhcp/
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/dhcp
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/systems/class_dhcpSystem.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dhcp/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dhcp/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dhcp/LICENSE


%files dns
%defattr(0644,root,root,755)
# Admin section
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/dns/class_DnsRecordAttribute.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/dns/class_dnsManagement.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/dns/class_dnsView.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/dns/class_dnsZone.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/dns/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/class_dnsHost.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/dnsrecords.tpl
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/dns/class_dnsAcl.inc
# Config section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/dns/class_dnsConfig.inc
# HTML section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/dns.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/dns.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/dns.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/dns.svg
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/dns
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dns/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dns/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dns/LICENSE


%files dovecot
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/dovecot/class_serviceDovecot.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/dovecot.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/dovecot.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/dovecot.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/dovecot.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/dovecot
# Personal section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/mail/mail-methods/class_mail-methods-dovecot.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dovecot/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dovecot/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dovecot/LICENSE


%files dsa
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/dsa/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/dsa/class_dsaManagement.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/dsa/class_simpleSecurityObject.inc
# Config section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/dsa/class_dsaConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/dsa.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/dsa.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/dsa.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/dsa.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/dsa
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dsa/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dsa/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dsa/LICENSE


%files fai
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/repository/fai_repository.tpl
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/repository/class_serviceRepository.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/class_faiLogView.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/class_faiStartup.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/class_faiProfile.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/class_faiTemplateEntry.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/class_faiPartitionTable.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/class_faiManagement.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/class_faiPackageConfiguration.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/class_faiTemplate.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/class_faiPartition.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/class_faiPackage.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/class_faiHook.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/class_faiVariable.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/class_faiDiskEntry.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/packageSelect/selectPackage-list.xml
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/packageSelect/class_filterFAIPackages.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/packageSelect/selectPackage-filter.xml
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/packageSelect/class_filterFAIcustoms.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/packageSelect/class_packageSelect.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/packageSelect/selectPackage-filter.tpl
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/class_faiScript.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/fai/class_faiSimplePluginClass.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/monitor/class_argonautFAIMonitor.inc
# Config section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/fai/class_faiConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/actions/package-configure.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/fai-hook.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/fai-packages.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/fai-partitiontable.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/fai-profile.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/fai-script.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/fai-template.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/fai-variable.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/fai.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/fai.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/actions/package-configure.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/fai-hook.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/fai-packages.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/fai-partitiontable.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/fai-profile.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/fai-script.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/fai-template.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/fai-variable.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/fai.svg
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/fai
# Documentation
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fai/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fai/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fai/LICENSE


%files freeradius
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/freeradius/class_freeradiusGroup.inc
# HTML section
# Directories
# Files in the directory
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/freeradius
# Personal section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/freeradius/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/freeradius/class_freeradiusAccount.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/freeradius.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/freeradius.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/freeradius.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/freeradius.png
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-freeradius/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-freeradius/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-freeradius/LICENSE


%files fusioninventory
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/fusioninventory/class_fiInventory.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/fusioninventory/class_fiInventoryAgent.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/fusioninventory/inventory.tpl
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/inventory/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/inventory/class_inventoryManagement.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/inventory/inventory-list.xml
# Config section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/fusioninventory/class_fiConfig.inc
# HTML section
%attr (-,root,root) %{_datadir}/fusiondirectory/html/collect.php
%attr (-,root,root) %{_datadir}/fusiondirectory/html/plugins/fusioninventory/inventory.css
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/fusioninventory.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/fusioninventory.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/fusioninventory.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/fusioninventory.png
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/fusioninventory
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fusioninventory/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fusioninventory/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fusioninventory/LICENSE


%files gpg
%defattr(0644,root,root,755)
# Addons section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/gpg/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/gpg/class_pgpServerInfo.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/gpg.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/gpg.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/gpg.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/gpg.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/gpg
# Personal section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/gpg/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/gpg/class_gpgAccount.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/gpg/pgpKeySelect/class_pgpKeySelect.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/gpg/pgpKeySelect/pgpKeySelect-list.xml
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-gpg/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-gpg/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-gpg/LICENSE


%files ipmi
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/ipmi/class_ipmiClient.inc
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/ipmi
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ipmi/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ipmi/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ipmi/LICENSE


%files ldapdump
%defattr(0644,root,root,755)
# Addons section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/ldapdump/class_ldapDump.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/ldapdump/ldapdump.tpl
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/ldapdump
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ldapdump/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ldapdump/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ldapdump/LICENSE


%files ldapmanager
%defattr(0644,root,root,755)
# Addons section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/ldapmanager/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/ldapmanager/class_csvimport.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/ldapmanager/tabs_ldif.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/ldapmanager/class_ldapmanager.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/ldapmanager.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/ldapmanager.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/ldapmanager.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/ldapmanager.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/ldapmanager
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ldapmanager/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ldapmanager/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ldapmanager/LICENSE


%files mail
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/groups/mail/class_mailGroup.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/systems/services/imap/class_serviceIMAP.inc
# Config section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/mail/class_mailPluginConfig.inc
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/mail
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/personal/mail/class_sieve.inc
# Personal section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/mail/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/mail/mailAddressSelect/class_mailAddressSelect.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/mail/class_mail-methods.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/mail/class_mailAccount.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/internet-mail.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/internet-mail.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/internet-mail.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/internet-mail.png
# HTML section
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/legacy/icons/16/apps/internet-mail.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/legacy/icons/48/apps/internet-mail.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/legacy/svg/internet-mail.svg
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-mail/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-mail/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-mail/LICENSE


%files nagios
%defattr(0644,root,root,755)
# Config section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/nagios/class_nagiosConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/nagios.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/nagios.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/nagios.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/nagios.png
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/nagios
# Personal section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/nagios/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/nagios/class_nagiosAccount.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-nagios/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-nagios/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-nagios/LICENSE


%files netgroups
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/netgroups/class_netgroupSystem.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/netgroups/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/netgroups/class_netgroupManagement.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/netgroups/memberNisnetgroupSelect/class_memberNisnetgroupSelect.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/netgroups/class_netgroup.inc
# Config section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/netgroups/class_netgroupConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/netgroups.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/netgroups.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/netgroups.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/netgroups.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/netgroups
# Personal section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/netgroups/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/netgroups/class_netgroupMembership.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-netgroups/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-netgroups/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-netgroups/LICENSE


%files opsi
%defattr(0644,root,root,755)
# Addons section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/opsi/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/opsi/opsiimport.tpl
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/addons/opsi/class_opsiImport.inc
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/opsi/class_serviceOPSI.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/opsi/class_opsiClient.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/opsi/class_opsiProfileManagement.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/opsi/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/opsi/class_opsiProfile.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/opsi/class_opsiProductProperties.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/opsi/class_opsiSoftwareList.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/opsi/class_opsiOnDemandList.inc
# Config section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/opsi/class_opsiConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/opsi.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/opsi.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/opsi.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/opsi.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/opsi-on-demand.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/opsi-software-list.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/opsi-on-demand.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/opsi-software-list.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/opsi-on-demand.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/opsi-software-list.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/opsi-on-demand.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/opsi-software-list.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/opsi
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-opsi/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-opsi/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-opsi/LICENSE


%files puppet
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/puppet/class_servicePuppet.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/puppet/class_puppetNode.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/puppet.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/puppet.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/puppet.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/puppet.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/puppet
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-puppet/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-puppet/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-puppet/LICENSE


%files pureftpd
%defattr(0644,root,root,755)
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/pureftpd.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/pureftpd.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/pureftpd.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/action.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/pureftpd
# Personal section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/pureftpd/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/pureftpd/class_pureftpdAccount.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-pureftpd/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-pureftpd/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-pureftpd/LICENSE


%files quota
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/quota/service_quota_parameters.tpl
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/quota/class_serviceQuota.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/quota.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/quota.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/quota.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/quota.svg

# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/quota
# Personal section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/quota/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/quota/quota_section.tpl
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/quota/class_quotaAccount.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-quota/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-quota/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-quota/LICENSE


%files repository
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/repository/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/repository/class_repositoryDistribution.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/repository/class_repositoryManagement.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/repository/class_repositorySection.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/repository/class_buildRepository.inc
# Config section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/repository/class_repositoryConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/repository-distribution.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/repository-section.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/repository.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/repository.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/puppet.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/repository-distribution.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/repository-section.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/repository.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/repository.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/repository
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-repository/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-repository/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-repository/LICENSE


%files samba
%defattr(0644,root,root,755)
# Admin section
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/samba/
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/samba/
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/groups/samba/
# Config section
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/samba/
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/samba/locale/
# Personal section
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/samba/
%attr (-,root,root) %{_datadir}/fusiondirectory/include/class_smbHash.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/samba.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/samba.svg
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-samba/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-samba/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-samba/LICENSE


%files sogo
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/sogo/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/sogo/class_sogoManagement.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/sogo/class_sogoResource.inc
# Config section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/sogo/class_sogoConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/sogo.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/sogo.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/sogo.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/sogo.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/sogo
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sogo/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sogo/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sogo/LICENSE


%files squid
%defattr(0644,root,root,755)
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/squid.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/squid.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/squid.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/squid.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/squid
# Personal section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/squid/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/squid/proxyAccount.tpl
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/squid/class_proxyAccount.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-squid/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-squid/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-squid/LICENSE


%files ssh
%defattr(0644,root,root,755)
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/ssh.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/ssh.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/ssh.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/ssh.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/ssh
# Personal section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/ssh/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/ssh/class_sshAccount.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ssh/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ssh/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ssh/LICENSE


%files sudo
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/sudo/usedoptions_section.tpl
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/sudo/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/sudo/class_sudoGeneric.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/sudo/class_sudoOption.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/sudo/tabs_sudo.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/sudo/class_sudoManagement.inc
# Config section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/sudo/class_sudoConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/sudo.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/sudo.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/sudo.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/sudo.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/sudo
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sudo/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sudo/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sudo/LICENSE


%files supann
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/supannStructures/class_supannStructuresManagement.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/supannStructures/class_entite.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/supannStructures/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/supannStructures/class_etablissement.inc
# Config section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/supann/class_supannConfig.inc
# Files contrib supann
%attr(-,root,root) %{_sysconfdir}/fusiondirectory/supann/corps
%attr(-,root,root) %{_sysconfdir}/fusiondirectory/supann/eturegimeinscription_SISE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/discipline_EXAMPLE
%attr(-,root,root) %{_sysconfdir}/fusiondirectory/supann/entite
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/etuelementpedagogique_EXAMPLE
%attr(-,root,root) %{_sysconfdir}/fusiondirectory/supann/diplome_SISE
%doc %attr(-,root,root) %{_sysconfdir}/fusiondirectory/supann/etablissement_SUPANN
%attr(-,root,root) %{_sysconfdir}/fusiondirectory/supann/role_SUPANN
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/etuetape_EXAMPLE
%attr(-,root,root) %{_sysconfdir}/fusiondirectory/supann/activite_CNU
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/diplome_EXAMPLE
%attr(-,root,root) %{_sysconfdir}/fusiondirectory/supann/activite_REFERENS
%attr(-,root,root) %{_sysconfdir}/fusiondirectory/supann/affiliation
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/typediplome_EXAMPLE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/eturegimeinscription_EXAMPLE
%attr(-,root,root) %{_sysconfdir}/fusiondirectory/supann/typediplome_SISE
%attr(-,root,root) %{_sysconfdir}/fusiondirectory/supann/discipline_SISE
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/supann-entite.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/supann-etablissement.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/supann.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/supann.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/supann.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/supann-entite.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/supann-etablissement.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/supann.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/supann
# Personal section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/supann/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/supann/student_subscription.tpl
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/supann/class_supannAccount.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/supannStructures/class_supann.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/LICENSE


%files sympa
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/sympa/class_serviceSympa.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/sympa/
# Config directory
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/sympa/
# HTML section
# Directories
# Files in the directory
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/sympa.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/sympa.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/sympa.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/sympa.svg
# Files
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/sympa
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sympa/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sympa/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sympa/LICENSE


%files systems
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/serverService-filter.xml
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/class_componentGeneric.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/class_systemManagement.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/class_systemImport.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/class_terminalStartup.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/class_serverGeneric.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/serverService-list.tpl
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/class_serverService.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/terminal/class_serviceTerminal.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/shares/service_share.tpl
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/shares/class_serviceShare.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/services/ldap/class_serviceLDAP.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/server_import.tpl
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/serverService-filter.tpl
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/class_mobilePhoneGeneric.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/class_terminalGeneric.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/system-list.xml
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/class_printGeneric.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/class_filterServerService.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/serverService-list.xml
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/class_workstationGeneric.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/tabs_server.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/class_phoneGeneric.inc
# Config section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/systems/class_systemsPluginConfig.inc
# Files
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/addons/dashboard/class_dashBoardNetwork.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/addons/dashboard/class_dashBoardSystems.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/addons/dashboard/network_dhcp.tpl
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/addons/dashboard/systems_pcids.tpl
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/addons/dashboard/systems_stats.tpl
# Locale section
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/systems/locale/
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/actions/task-schedule.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/actions/task-start.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/actions/task-stop.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/actions/view-logs.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/places/folder-network.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/svg/clock.svg
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/svg/server_locked.svg
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/svg/service_apache.svg
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/svg/service_file.svg
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/svg/service_ldap.svg
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/svg/status_start.svg
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/svg/status_stop.svg
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/svg/terminal_locked.svg
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/svg/view_logs.svg
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/svg/workstation_locked.svg
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/legacy/icons/16/actions/media-playback-start.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/legacy/icons/16/actions/media-playback-stop.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/legacy/icons/16/places/folder-remote.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/legacy/svg/folder-remote.svg
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/legacy/svg/media-playback-start.svg
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/legacy/svg/media-playback-stop.svg
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-systems/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-systems/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-systems/LICENSE


%files weblink
%defattr(0644,root,root,755)
# Admin section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/systems/weblink/class_webLink.inc
# Locale section
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/weblink
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-weblink/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-weblink/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-weblink/LICENSE


%files webservice
%defattr(0644,root,root,755)
# Config section
# Files
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/class_webserviceConfig.inc
# Locales
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/
# Files
%{_datadir}/fusiondirectory/include/jsonrpcphp/jsonRPCServer.php
%attr (-,root,root) %{_datadir}/fusiondirectory/html/jsonrpc.php
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-webservice/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-webservice/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-webservice/LICENSE

%files ejbca
%defattr(0644,root,root,755)
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/ejbca/class_ejbcaCertificate.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/ejbca/class_ejbcaManagement.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/ejbca/main.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/ejbca/class_ejbcaCertSelect.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/ejbca/certificates/class_ejbcaCertificates.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/ejbca/certificates/main.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/config/ejbca/class_ejbcaConfig.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/ejbca.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/ejbca.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/ejbca.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/ejbca.svg
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ejbca/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ejbca/LICENSE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ejbca/Changelog

%files applications
%defattr(0644,root,root,755)
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/applications/class_applicationGeneric.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/applications/class_applicationManagement.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/applications/class_webApplication.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/applications/main.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/roles/class_applicationRights.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/config/applications/class_applicationsPluginConfig.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/plugins/applications/images/default_icon.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-applications/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-applications/LICENSE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-applications/Changelog

%files personal
%defattr(0644,root,root,755)
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/personal/personal/class_personalInfo.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/personal/personal/class_socialHandlers.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/personal/personal/main.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/config/personal/class_personalConfig.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-personal/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-personal/LICENSE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-personal/Changelog


%files ppolicy
%defattr(0644,root,root,755)
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ppolicy/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ppolicy/LICENSE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ppolicy/Changelog
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/ppolicy/class_ppolicy.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/ppolicy/class_ppolicyManagement.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/ppolicy/main.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/config/ppolicy/class_ppolicyConfig.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/personal/ppolicy/class_ppolicyAccount.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/personal/ppolicy/main.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/addons/dashboard/class_dashBoardPPolicy.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/addons/dashboard/ppolicy_locked_accounts.tpl
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/ppolicy.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/ppolicy.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/ppolicy.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/ppolicy.svg
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ppolicy/locale/
%attr (-,root,root)     %{_datadir}/doc/fusiondirectory-plugin-ppolicy/ppolicyconfig.ldif
%attr (-,root,root)     %{_datadir}/doc/fusiondirectory-plugin-ppolicy/ppolicymodule.ldif

%files certificates
%defattr(0644,root,root,755)
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-certificates/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-certificates/LICENSE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-certificates/Changelog
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/certificates/locale/
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/personal/certificates/class_userCertificates.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/personal/certificates/main.inc

%files mixedgroups
%defattr(0644,root,root,755)
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-mixedgroups/AUTHORS.md
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-mixedgroups/LICENSE
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-mixedgroups/Changelog
%attr (-,root,root)      %{_datadir}/fusiondirectory/locale/plugins/mixedgroups/locale/
%attr (-,root,root)      %{_datadir}/fusiondirectory/plugins/admin/ogroups/mixedgroups/class_mixedGroup.inc

%files subcontracting
%defattr(0644,root,root,755)
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-subcontracting/AUTHORS.md
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-subcontracting/LICENSE
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-subcontracting/Changelog
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/subcontracting.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/subcontracting.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/subcontracting.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/subcontracting.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/subcontracting/locale/
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/subcontracting/class_subContracting.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/subcontracting/main.inc

%files newsletter
%defattr(0644,root,root,755)
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/newsletter/locale/
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/newsletter/class_newsletterConfig.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/newsletter/class_newsletterSubscriptions.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/personal/newsletter/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/newsletter.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/newsletter.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/newsletter.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/newsletter.png
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-newsletter/AUTHORS.md
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-newsletter/LICENSE
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-newsletter/Changelog

%files community
%defattr(0644,root,root,755)
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/departments/community/class_communityOrganization.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/admin/departments/community/class_communityProject.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/plugins/config/community/class_communityConfig.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/community.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/community.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/community.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/community.png
%attr (-,root,root) %{_datadir}/fusiondirectory/locale/plugins/community/locale/
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-community/AUTHORS.md
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-community/LICENSE
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-community/Changelog

%files postfix
%defattr(0644,root,root,755)
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/systems/services/postfix/class_servicePostfix.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/postfix/locale/
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/smtp.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/smtp.svg
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-postfix/AUTHORS.md
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-postfix/LICENSE
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-postfix/Changelog

%files spamassassin
%defattr(0644,root,root,755)
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/systems/services/spam/class_serviceSpamAssassin.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/spamassassin/locale/
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/personal/spamassassin/class_spamAssassinAccount.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/personal/spamassassin/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/spamassassin.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/spamassassin.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/spamassassin.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/spamassassin.svg
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-spamassassin/AUTHORS.md
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-spamassassin/LICENSE
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-spamassassin/Changelog

%files user-reminder
%defattr(0644,root,root,755)
%doc %attr (-,root,root)     %{_datadir}/doc/fusiondirectory-plugin-user-reminder/AUTHORS.md
%doc %attr (-,root,root)     %{_datadir}/doc/fusiondirectory-plugin-user-reminder/LICENSE
%doc %attr (-,root,root)     %{_datadir}/doc/fusiondirectory-plugin-user-reminder/Changelog
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/user-reminder/locale/
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/config/user-reminder/class_userReminderConfig.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/class_expiredUserPostpone.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/expired_postpone.php
%attr (-,root,root)     %{_datadir}/fusiondirectory/ihtml/themes/breezy/user-reminder.tpl


%files audit
%defattr(0644,root,root,755)
%doc %attr (-,root,root)     %{_datadir}/doc/fusiondirectory-plugin-audit/AUTHORS.md
%doc %attr (-,root,root)     %{_datadir}/doc/fusiondirectory-plugin-audit/LICENSE
%doc %attr (-,root,root)     %{_datadir}/doc/fusiondirectory-plugin-audit/Changelog
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/audit/class_auditEvent.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/config/audit/class_auditConfig.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/audit/locale/
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/audit/class_auditManagement.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/audit/main.inc
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/audit.png
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/audit.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/svg/48/apps/audit.svg
%attr (-,root,root) %{_datadir}/fusiondirectory/html/themes/breezy/icons/48/apps/audit.png

%files renater-partage
%defattr(0644,root,root,755)
%doc %attr (-,root,root)     %{_datadir}/doc/fusiondirectory-plugin-renater-partage/AUTHORS.md
%doc %attr (-,root,root)     %{_datadir}/doc/fusiondirectory-plugin-renater-partage/LICENSE
%doc %attr (-,root,root)     %{_datadir}/doc/fusiondirectory-plugin-renater-partage/Changelog
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/systems/services/renater-partage/
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/groups/renater-partage/
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/renater-partage/locale/
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/personal/mail/mail-methods/class_mail-methods-renater-partage.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/icons/16/apps/renater-partage.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/themes/breezy/svg/16/apps/renater-partage.svg

%files posix
%defattr(0644,root,root,755)
%doc %attr (-,root,root)     %{_datadir}/doc/fusiondirectory-plugin-posix/AUTHORS.md
%doc %attr (-,root,root)     %{_datadir}/doc/fusiondirectory-plugin-posix/LICENSE
%doc %attr (-,root,root)     %{_datadir}/doc/fusiondirectory-plugin-posix/Changelog
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/posix/locale/
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/groups/posix/
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/config/posix/
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/personal/posix/


%files alias-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/alias-fd-conf.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/alias-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-alias-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-alias-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-alias-schema/LICENSE


%files argonaut-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/argonaut-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-argonaut-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-argonaut-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-argonaut-schema/LICENSE


%files autofs-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/autofs-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-autofs-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-autofs-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-autofs-schema/LICENSE


%files cyrus-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/cyrus-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-cyrus-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-cyrus-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-cyrus-schema/LICENSE


%files debconf-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/debconf.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/debconf-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-debconf-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-debconf-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-debconf-schema/LICENSE


%files dhcp-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/dhcp-fd.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/dhcp-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dhcp-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dhcp-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dhcp-schema/LICENSE


%files dns-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/dns-fd-conf.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/dnszone.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/dns-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dns-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dns-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dns-schema/LICENSE


%files dovecot-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/dovecot-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dovecot-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dovecot-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dovecot-schema/LICENSE


%files dsa-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/dsa-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dsa-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dsa-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dsa-schema/LICENSE


%files fai-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/fai.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/fai-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fai-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fai-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fai-schema/LICENSE


%files freeradius-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/freeradius.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-freeradius-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-freeradius-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-freeradius-schema/LICENSE


%files fusioninventory-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/inventory-fd.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/fusioninventory-fd.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/fusioninventory-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fusioninventory-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fusioninventory-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fusioninventory-schema/LICENSE


%files gpg-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/pgp-recon.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/pgp-keyserver.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/pgp-remte-prefs.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/gpg-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-gpg-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-gpg-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-gpg-schema/LICENSE


%files ipmi-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/ipmi-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ipmi-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ipmi-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ipmi-schema/LICENSE


%files mail-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/mail-fd-conf.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/mail-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-mail-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-mail-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-mail-schema/LICENSE


%files nagios-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/nagios-fd-conf.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/netways.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-nagios-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-nagios-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-nagios-schema/LICENSE


%files netgroups-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/netgroups-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-netgroups-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-netgroups-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-netgroups-schema/LICENSE


%files opsi-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/opsi-fd.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/opsi-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-opsi-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-opsi-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-opsi-schema/LICENSE


%files puppet-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/puppet.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/puppet-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-puppet-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-puppet-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-puppet-schema/LICENSE


%files pureftpd-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/pureftpd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-pureftpd-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-pureftpd-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-pureftpd-schema/LICENSE


%files quota-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/quota.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/quota-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-quota-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-quota-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-quota-schema/LICENSE


%files repository-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/repository-fd.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/repository-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-repository-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-repository-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-repository-schema/LICENSE


%files samba-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/samba-fd-conf.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/samba.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-samba-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-samba-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-samba-schema/LICENSE


%files sogo-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/sogo-fd-conf.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/calRessources.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/calEntry.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sogo-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sogo-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sogo-schema/LICENSE


%files squid-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/proxy-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-squid-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-squid-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-squid-schema/LICENSE


%files ssh-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/openssh-lpk.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ssh-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ssh-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ssh-schema/LICENSE


%files sudo-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/sudo-fd-conf.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/sudo.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sudo-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sudo-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sudo-schema/LICENSE


%files supann-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/internet2.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/supann_2009.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/supann-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann-schema/LICENSE


%files sympa-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/sympa-fd.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/sympa-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sympa-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sympa-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sympa-schema/LICENSE


%files systems-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/systems-fd-conf.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/systems-fd.schema
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/service-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-systems-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-systems-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-systems-schema/LICENSE


%files weblink-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/weblink-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-weblink-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-weblink-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-weblink-schema/LICENSE


%files webservice-schema
%defattr(0644,root,root,755)
# Files
%attr (-,root,root) %{_sysconfdir}/openldap/schema/fusiondirectory/webservice-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-webservice-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-webservice-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-webservice-schema/LICENSE

%files applications-schema
%defattr(0644,root,root,755)
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/applications-fd-conf.schema
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/applications-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-applications-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-applications-schema/LICENSE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-applications-schema/Changelog

%files ejbca-schema
%defattr(0644,root,root,755)
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/ejbca-fd-conf.schema
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/ejbca-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ejbca-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ejbca-schema/LICENSE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ejbca-schema/Changelog

%files personal-schema
%defattr(0644,root,root,755)
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/personal-fd.schema
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/personal-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-personal-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-personal-schema/LICENSE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-personal-schema/Changelog

%files ppolicy-schema
%defattr(0644,root,root,755)
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/ppolicy-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ppolicy-schema/AUTHORS.md
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ppolicy-schema/LICENSE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ppolicy-schema/Changelog

%files subcontracting-schema
%defattr(0644,root,root,755)
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/subcontracting-fd.schema
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-subcontracting-schema/AUTHORS.md
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-subcontracting-schema/LICENSE
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-subcontracting-schema/Changelog

%files newsletter-schema
%defattr(0644,root,root,755)
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/newsletter-fd-conf.schema
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/newsletter-fd.schema
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-newsletter-schema/AUTHORS.md
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-newsletter-schema/LICENSE
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-newsletter-schema/Changelog

%files community-schema
%defattr(0644,root,root,755)
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/community-fd-conf.schema
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/community-fd.schema
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-community-schema/AUTHORS.md
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-community-schema/LICENSE
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-community-schema/Changelog

%files postfix-schema
%defattr(0644,root,root,755)
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/postfix-fd.schema
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-postfix-schema/AUTHORS.md
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-postfix-schema/LICENSE
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-postfix-schema/Changelog

%files spamassassin-schema
%defattr(0644,root,root,755)
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/spamassassin-fd.schema
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-spamassassin-schema/AUTHORS.md
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-spamassassin-schema/LICENSE
%doc %attr(-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-spamassassin-schema/Changelog

%files user-reminder-schema
%defattr(0644,root,root,755)
%attr (-,root,root)       %{_sysconfdir}/openldap/schema/fusiondirectory/user-reminder-fd-conf.schema
%doc %attr (-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-user-reminder-schema/AUTHORS.md
%doc %attr (-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-user-reminder-schema/LICENSE
%doc %attr (-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-user-reminder-schema/Changelog

%files audit-schema
%defattr(0644,root,root,755)
%attr (-,root,root)       %{_sysconfdir}/openldap/schema/fusiondirectory/audit-fd-conf.schema
%attr (-,root,root)       %{_sysconfdir}/openldap/schema/fusiondirectory/audit-fd.schema
%doc %attr (-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-audit-schema/AUTHORS.md
%doc %attr (-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-audit-schema/LICENSE
%doc %attr (-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-audit-schema/Changelog

%files renater-partage-schema
%defattr(0644,root,root,755)
%attr (-,root,root)       %{_sysconfdir}/openldap/schema/fusiondirectory/renater-partage-fd.schema
%doc %attr (-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-renater-partage-schema/AUTHORS.md
%doc %attr (-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-renater-partage-schema/LICENSE
%doc %attr (-,root,root)  %{_datadir}/doc/fusiondirectory-plugin-renater-partage-schema/Changelog

########################

%changelog
* Sat Sep 01 2018 Jonathan SWAELENS <jonathan@opensides.be> - 1.2.2-1
- [Changed] fusiondirectory#5690 AUTHORS as been Renamed AUTHORS.md
- [Changed] fusiondirectory#5692 Change the partage icon to be the new one

* Mon Jun 11 2018 Jonathan SWAELENS <jonathan@opensides.be> - 1.2.1-1
- [Changed] fusiondirectory#5666 Change file COPYING into LICENCE
- [Changed] fusiondirectory#5673 Adapt packages for stuff that are moved to dev-tools

* Mon Jul 24 2017 Jonathan SWAELENS <jonathan@opensides.be> - 1.3-1
- Fixes #5658 Fixed spec file for new plugins folders organization

* Tue Jun 27 2017 Jonathan SWAELENS <jonathan@opensides.be> - 1.2-1
- Fixes #5613 Rename class_groupMail.inc in class_mailGroup.inc
- Fixes #5605 Remove alias plugin from sympa dependance and add some files
- Fixes #5609 Add class_partageGroup.inc
- Fixes #5618 Correct the date error in changelog
- Fixes #5621 Correct specfile with rpmlint help
- Fixes #5643 Remove contentcsv.tpl

* Tue Jun 06 2017 Jonathan SWAELENS <jonathan@opensides.be> - 1.1.1-1
- New upstream release

* Wed May 17 2017 Jonathan SWAELENS <jonathan@opensides.be> - 1.1-2
- Add php54-php-Smarty3-gettext as dependance

* Fri Apr 28 2017 Jonathan SWAELENS <jonathan@opnesides.be> - 1.1-1
- Fixes #5111 Remove few files not used for DHCP plugin
- Fixes #5116 Package packageSelect class for FAI
- Fixes #5120 Redone systemManagement with simpleManagement
- Fixes #5126 dhcp/config/dhcp/class_dhcpConfig.inc is missing from the package
- Fixes #5338 Remove kolab2 plugin
- Fixes #5390 Remove argonaut dependence for systems plugin
- Fixes #5416 Remove old legacy icons and replace it with tango icon
- Fixes #5417 Remove class_dhpcHost in systems
- Fixes #5418 Remove unused files for netgroups
- Fixes #5419 Remove ppolicydefault.ldif
- Fixes #5420 Remove dhcpd.schema
- Fixes #5353 Package renater-partage plugin
- Fixes #5407 Package posix plugin
- Fixes #5376 Add dependence between SSH plugin and Posix plugin
- Fixes #5496 Add dependance between samba plugin and posix plugin
- Fixes #5501 Update specfile to make samba plugin more dependant of directories in place of files

* Mon Apr 03 2017 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.20-1
- New upstream release

* Fri Jan 20 2017 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.19-1
- New upstream release

* Mon Jan 16 2017 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.18-1
- Fixes #5304 Remove unused files for netgroups
- Fixes #5116 FAI packageSelect use simpleSelectManagement

* Mon Nov 14 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.17-1
- Fixes #5202 Revert remove dependance between systems and dhcp
- Fixes #5215 adding files for dhcp packages
- Fixes #5209 adding dhcp-fd-conf.schema
- Fixes #5202 Remove dependance between systems and dhcp
- Fixes #5222 Remove ppolicydefault.ldif from ppolicy packages

* Thu Sep 29 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.16-1
- Fixes #5167 Remove old legacy icons and replace it with tango icon

* Tue Aug 23 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.15-1
- Fixes #5065 Add update samba share action in samba plugin
- Fixes #5078 Remove apache2 plugin
- Fixes #5083 Remove phoneSelect directory
- Fixes #5065 Add class_argonautEventTypes.inc file
- Fixes #5061 Use simple plugin for GPG

* Mon Jul 04 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.14-1
- Fixes #4977 Add service generic IMAP server
- Fixes #4930 Plugins use some image that are not in theme
- Fixes #4940 Rename default theme as legacy
- Fixes #4950 Remove game plugin
- Fixes #4895 Remove printGeneric.tpl and ppd folder
- Fixes #4860 Package more Breezy's icons

* Mon Jun 13 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.13-1
- Removing no longer used images
- Adding theme for game plugin
- Corrected icon to be autofs-nis-netmap in place of autofs-nis-map
- Fixes #4860 Package Breezy's icons
- Fixes #4837 Package audit plugin
- Fixes #4815 Remove config(noreplace) for schema packages
- Fixes #4812 Package user-reminder plugin
- Fixes #4786 Split specfile rhel6 and rhel7 to modify the php dependence of rhel6
- Fixes #4780 Remove Replace kolab ogroup tab and remove unused goService class
- Fixes #4780 Remove addressbook plugin

* Fri May 13 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.12-3
- Fixes #4786 Split specfile rhel6 and rhel7 to modify the php dependence of rhel6

* Tue May 10 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.12-2
- New upstream release

* Tue May 03 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.12-1
- Fixes #4750 Add files for plugin spamassassin
- Fixes #4718 Adapt the dependences due the splitting of the mail plugin
- Fixes #4732 Remove class_serviceIMAP.inc
- Fixes #4710 Removing of another 's'
- Fixes #4710 We missed some "s" sometimes
- Fixes #4710 Replace spamassasin with spamassassin
- Fixes #4710 Move spamassasin service in his own plugin
- Fixes #4703 Move postfix service in his own plugin
- Fixes #4696 Remove antivirus service from mail plugin

* Thu Apr 07 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.11-1
- Fixes #4670 Some files have been removed related to community plugin

* Tue Mar 15 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.10-1
- Fixes #4500 Remove unused nagios.tpl file
- Fixes #4471 Remove the dependence between systems and dns
- Fixes #4547 Remove old files for DNS plugin
- Fixes #4552 Remove NTP service
- Fixes #4361 Add dns-fd.schema
- Fixes #4547 Add new files for the new DNS plugin
- Fixes #4547 Forgot 2 files got the new DNS plugin
- Fixes #4536 Package subcontracting plugin
- Fixes #4536 Syntax error in the spec file
- Fixes #4547 Move the icons in the right folder for the plugin DNS
- Fixes #4547 Add an elif for DNS plugin
- Fixes #4536 Move the icons for subcontracting plugin
- Fixes #4536 Modify path for subcontracting icons
- Fixes #4536 Correct errors in the path for subcontracting icons
- Fixes #4587 Add newsletter plugin
- Fixes #4582 Add community plugin
- Fixes #4596 Modify spec file to copy html images in the good path
- Fixes #4596 Modification for fusioninventory plugin in the spec file
- Fixes #4596 Recreate a directory for fusioninventory plugin that I had remove by error
- Fixes #4596 Correct paths of many plugins in the spec file
- Fixes #4596 Add a section to copy the images of fusiondirectory-plugin-game
- Fixes #4617 Package getFAIstatus.php
- Fixes #4617 Forgot to add the file in the %files section
- Fixes #4596 Forgot some icons for repository plugin
- Fixes #4596 Remove unused images for systems plugin
- Fixes #4596 Add some opsi icons
- Fixes #4547 Add class_dnsAcl.inc

* Mon Feb 01 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.9.3-1
- New upstream release

* Wed Jan 06 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.9.2-1
- Fixes #4228 Move the supann example in an example directory
- Fixes #4243 Add update cache and update locales for applications
- Fixes #4333 Move the icons of ppolicy plugin
- Fixes #4338 Move exemple ldif of ppolicy in /usr/share/doc/fusiondirectory-plugin-ppolicy/
- Fixes #4369 Remove rsyslog plugin
- Fixes #4330 Add version for fusiondirectory-plugin-systems-schema dependance
- Fixes #4283 Add version for fusiondirectory-plugin-systems dependance
- Fixes #4276 Add dependance between sudo and systems
- Fixes #4405 Clean up the DaemonEvent mess
- Fixes #4397 Remove the mail method Cyrus Sendmail
- Fixes #4416 Migrate last FAI classes to simplePlugin
- Fixes #4416 Forgot to remove faiDiskEntry.tpl
- Fixes #4405 Add class_argonautAction.inc and import_events.tpl
- Fixes #4416 Add class_faiDiskEntry.inc in specfile
- Fixes #4427 Remove fix_munged from the samba plugin
- Fixes #4421 Remove the class_BootKernelAttribute.inc

* Thu Oct 8 2015 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.9.1-1.el6
- Fixes #4136 Add class_smbHash in fusiondirectory-plugin-samba
- Fixes #4136 Add samba.schema in fusiondirectory-plugin-samba-schema

* Thu Sep 24 2015 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.9-1.el6
- Remove unused password.tpl
- Update locales for applications, certificates, ejbca, personal, ppolicy and webservice
- Set good path for dhcp icon
- Remove class_phoneIAX.inc and class_asteriskAccount.inc from asterisk plugin
- Dashboard is merged in core
- Remove desktop-management plugin
- Remove old patch of goticus
- Remove openstack plugin
- Remove uw-imap plugin
- Add applications, ejbca, personal and ppolicy plugin
- Add asteriskcdrdb.sql
- Add sieve_add png in mail plugin
- Add locales for applications, certificates, ejbca, personal, ppolicy and webservice
- Add dashboard part in systems
- Rewrite a part of asterisk plugin
- Correction of sieve support in cyrus and mail plugin
- Missed class_supann.inc
- Remove class_tabs.inc
- Add mixedgroups plugin
- Remove the fax plugin
- Remove the asterisk plugin
- Fixes #4080 Add directory mode 755
- Fixes #4077 Package FAI monitor service in plugin FAI
- Rename role file in role_SUPANN (#4075)
- Rename kolab to kolab2
- Fixes #4133 Add argonaut plugin dependence for system plugin

* Thu Jul 30 2015 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.8.9-1.el6
- New upstream release

* Tue Jun 30 2015 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.8.8-1.el6
- Add schemas dependences

* Fri Jun 05 2015 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.8.7-1.el6
- New upstream release

* Mon Jun 01 2015 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.8.6-1.el6
- Correct the place of EJBCA icon's
- Add plugin certificates

* Thu Apr 02 2015 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.8.5-1.el6
- Move dashbord in core
- Add locales for ppolicy plugin
- Add ppolicy plugin
- Add some files for personal plugin

* Sat Dec 13 2014 Jonathan SWAELENS <FD.K1412@openaliasbox.org> - 1.0.8.3-1.el6
- Add personal plugin
- Move the examples from supann plugin

* Tue Apr 1 2014 Jonathan SWAELENS <FD.K1412@openaliasbox.org> - 1.0.7.3-2.el6
- Add scriptaculous and prototype in the requires
- Add the patches for headers.tpl and password.tpl

* Mon Mar 31 2014 Jonathan SWAELENS <FD.K1412@openaliasbox.org> - 1.0.7.3-2.el6
- Adapt the scripts and patchs for the version 1.0.7.3

* Sun Jun 09 2013 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.6-2.el6
- Reorganize include directory files declaration in order to avoid multiple
  declaration in serveral RPMS (Closes #2504)
- Move the config/systems directory from sympa plugin to systems plugin (Closes #2423)
- Move the class_mailPluginConfig.inc file from core RPM to mail plugin (Closed #2485)
- Backport bugfix #2424 : Try to use PHP hash function if mhash is not available.
- Backport bugfix #2449 : Allow users with SAMBA attributes to be deleted properly.

* Sun May 12 2013 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.6-1.el6
- Upgrade to 1.0.6 Version
- Schema are now only provided in .schema format
- Plugins reorganisation and simplification
- Gofax plugin new name : fax
- Gofon plugin new name : asterisk
- Obsolete plugins removed : netatalk, opengroupware,openxchange,pptp, phpschedule-it, webdav, connectivity, scalix
- New plugins : alias, autofs, cyrus, debconf, DSA, freeradius, game, opsi, puppet

* Fri Nov 23 2012 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.4-1
- Upgrade to 1.0.4 Version
- Remove Obsoletes directives
- Remove devel package
- Update default apache configuration. Memory size set to 128M.
- Dependency list update
- New package : database-management
- Update scripts integration.

* Sat Jul 14 2012 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.3-2
- Move Lost Password Feature files from argonaut plugin to core RPM - Closes #1161

* Sat Jun 23 2012 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.3-1.el6
- Upgrade to 1.0.3 Version
- New plugins : argonaut, openstack-compute, quota, supann
- Merge goto plugin into system plugin
- Remove obsolete plugins : php54-gw
- Remove obsolete patches
- Add missing dependency on perl-ExtUtils-MakeMaker
- SELinux policy update
- Update memory_limite parameter in the Apache Configuration file
- Remove the spool purge cleaning step in %%pre and %%postun steps
- Add devel package

* Sun Oct 23 2011 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.2-1
- Upgrade to 1.0.2 Version
- [rpm] SELinux policy update
- [rpm] Mail Queue Plugin disabled
- [rpm] Patch for get_i18n and get_classs method on fusiondirectory-setup
- [rpm] Patch for removing debug messages
- [feature] Remove online doc
- [feature] Add netgroups plugin
- [feature] Removed old GOsa-si code
- [feature] Added jsonrpc client library
- [feature] Added new daemon class with json rpc methods
- [feature] All deployment are now done through the Argonaut json rpc server
- [feature] New system to get the packages and debconf without a local mirror
- [fix] Cvs import fixes to make it more flexible and usable
- [fix] Corrected css for Firefox 5 and beyond
- [feature] New setup command fusiondirectory-setup that help fixes common setup issues
- [feature] Added tools to easily convert and upload schema in an ldap-tree
- [feature] Completely test and rewrote the help to use php safe mode
- [feature] Put all the application data into /var/cache/fusiondirectory
- [fix] Fixed timezone issues
- [fix] Corrected FSF address
- [feature] Removed the opsi (pending rewrite)
- [feature] Removed log plugin, everything is done with the rsyslog plugin

* Sun Jul 03 2011 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.1-3
- Compliancy to Fedora Policy (fc15)
- Remove gosa-ldap Obsoletes block

* Sat Jun 18 2011 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.1-2
- Fixes #308: Remove the heimdal package
- Fixes #309: Remove the goAgent.pl from plugin-squid package

* Mon May 09 2011 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.1-1
- Update to 1.0.1 version
- Remov advanced options from setup
- Correct online help
- Correct wording on plugins
- Remove the need for magic_quotes_gpc
- Remove the fusiondirectory-desktop package
- Remove program version checking from svn
- Add the apache plugin
- Put final logo
- Full italian language
- Creation of the fusiondirectory SELinux package
- Fixes bugs #104 #118 #154 #163 #187 #188 #189 #191 #192 #193
- Fixes bugs #194 #197 #198 #199 #207 #208 #210 #217 #224 #230
- Fixes bugs #234 #251 #252

* Sun Apr 17 2011 Olivier BONHOMME <obonhomme@nerim.net> - 1.0-1
- First Plugin integration
- Update packager identity

* Fri Apr 15 2011 Benoit Mortier <benoit.mortier@opensides.be>
- First build of FusionDirectory 1.0 as an RPM, should work on SuSE and RedHat
