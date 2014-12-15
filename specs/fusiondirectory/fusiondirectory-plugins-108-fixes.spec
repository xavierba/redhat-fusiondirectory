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

%description 
FusionDirectory is a combination of system-administrator and end-user web
interface, designed to handle LDAP based setups.
Provided is access to posix, shadow, samba, proxy, fax, and Kerberos
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
    mkdir -p %{buildroot}%{_datadir}/fusiondirectory/plugins/
    mkdir -p %{buildroot}%{_datadir}/fusiondirectory/html/plugins/debug-help
    cp -a ./CODING %{buildroot}%{_datadir}/doc/fusiondirectory-developers/
    cp -a ./Doxyfile %{buildroot}%{_datadir}/doc/fusiondirectory-developers/
    cp -a ./FDStandard %{buildroot}%{_datadir}/doc/fusiondirectory-developers/
    cp -a ./filter.xsd  %{buildroot}%{_datadir}/doc/fusiondirectory-developers/
    cp -a ./list.xsd %{buildroot}%{_datadir}/doc/fusiondirectory-developers/
    cp -a ./simple-plugin %{buildroot}%{_datadir}/doc/fusiondirectory-developers/
    cp -a ./debug-help %{buildroot}%{_datadir}/fusiondirectory/plugins/
    cp -a ./debug-help/html/images %{buildroot}%{_datadir}/fusiondirectory/html/plugins/debug-help
    
  else
    # Addons section
    if [ -d ./addons ] ; then
      mkdir -p %{buildroot}%{_datadir}/fusiondirectory/plugins/addons/
      
      # Directories
      for cur_addons in $(find ./addons -mindepth 1 -maxdepth 1 -type d) ; do
        addons_line="$(echo ${cur_addons} | sed "s#./addons/##")" 
        cp -a ./addons/${addons_line} %{buildroot}%{_datadir}/fusiondirectory/plugins/addons/
      done
    
      # Files
      for cur_addons in $(find ./addons -mindepth 1 -maxdepth 1 -type f) ; do
        addons_line="$(echo ${cur_addons} | sed "s#./addons/##")" 
        cp -a ./addons/${addons_line} %{buildroot}%{_datadir}/fusiondirectory/plugins/addons/
      done
    fi
    
    
    # Admin section
    if [ -d ./admin ] ; then
      mkdir -p %{buildroot}%{_datadir}/fusiondirectory/plugins/admin/
    
      # Directories
      for cur_admin in $(find ./admin -mindepth 1 -maxdepth 1 -type d) ; do
        admin_line="$(echo ${cur_admin} | sed "s#./admin/##")" 
        cp -a ./admin/${admin_line} %{buildroot}%{_datadir}/fusiondirectory/plugins/admin/
      done
    
      # Files
      for cur_admin in $(find ./admin -mindepth 1 -maxdepth 1 -type f) ; do
        admin_line="$(echo ${cur_admin} | sed "s#./admin/##")" 
        cp -a ./admin/${admin_line} %{buildroot}%{_datadir}/fusiondirectory/plugins/admin/${admin_line}
      done
    fi
    
    
    # Config section
    if [ -d ./config ] ; then
      mkdir -p %{buildroot}%{_datadir}/fusiondirectory/plugins/config/
    
      # Directories
      for cur_config in $(find ./config -mindepth 1 -maxdepth 1 -type d) ; do
        config_line="$(echo ${cur_config} | sed "s#./config/##")" 
        cp -a ./config/${config_line} %{buildroot}%{_datadir}/fusiondirectory/plugins/config/
      done

      # Files
      for cur_config in $(find ./config -mindepth 1 -maxdepth 1 -type f) ; do
        config_line="$(echo ${cur_config} | sed "s#./config/##")" 
        cp -a ./config/${config_line} %{buildroot}%{_datadir}/fusiondirectory/plugins/config/
      done
    fi
    
    
    # HTML section
    if [ -d ./html ] ; then
      if [ "${cur_plugin}" = "addressbook" ] ; then
        mkdir -p %{buildroot}%{_datadir}/fusiondirectory/html/plugins/${cur_plugin}/
        cp -a ./html/images/ %{buildroot}%{_datadir}/fusiondirectory/html/plugins/${cur_plugin}/
        cp -a ./html/getvcard.php %{buildroot}%{_datadir}/fusiondirectory/html/plugins/${cur_plugin}/
        
      elif [ "${cur_plugin}" = "argonaut" ] ; then
        mkdir -p %{buildroot}%{_datadir}/fusiondirectory/html/plugins/${cur_plugin}/
        cp -a ./html/images/ %{buildroot}%{_datadir}/fusiondirectory/html/plugins/${cur_plugin}/
        
      elif [ "${cur_plugin}" = "fax" ] ; then
        mkdir -p %{buildroot}%{_datadir}/fusiondirectory/html/plugins/${cur_plugin}/
        cp -a ./html/images/ %{buildroot}%{_datadir}/fusiondirectory/html/plugins/${cur_plugin}/
        cp -a ./html/getfax.php %{buildroot}%{_datadir}/fusiondirectory/html/plugins/${cur_plugin}/
        
      elif [ "${cur_plugin}" = "fusioninventory" ] ; then
        mkdir -p %{buildroot}%{_datadir}/fusiondirectory/html/
        mkdir -p %{buildroot}%{_datadir}/fusiondirectory/html/plugins/${cur_plugin}/
        cp -a ./html/collect.php %{buildroot}%{_datadir}/fusiondirectory/html/
        cp -a ./html/images/ %{buildroot}%{_datadir}/fusiondirectory/html/plugins/${cur_plugin}/
        cp -a ./html/plugins/inventory.css %{buildroot}%{_datadir}/fusiondirectory/html/plugins/${cur_plugin}/
        
      else
        # Directories
        for cur_html in $(find ./html -mindepth 1 -maxdepth 1 -type d) ; do
          mkdir -p %{buildroot}%{_datadir}/fusiondirectory/html/plugins/${cur_plugin}/
          html_line="$(echo ${cur_html} | sed "s#./html/##")" 
          cp -a ./html/${html_line} %{buildroot}%{_datadir}/fusiondirectory/html/plugins/${cur_plugin}/
        done

        # Files
        for cur_html in $(find ./html -mindepth 1 -maxdepth 1 -type f) ; do
          mkdir -p %{buildroot}%{_datadir}/fusiondirectory/html/
          html_line="$(echo ${cur_html} | sed "s#./html/##")" 
          cp -a ./html/${html_line} %{buildroot}%{_datadir}/fusiondirectory/html/
        done
      fi
    fi
    
    
    # Include section
    if [ -d ./include ] ; then
      mkdir -p %{buildroot}%{_datadir}/fusiondirectory/include/    
      # Directories
      for cur_include in $(find ./include -mindepth 1 -maxdepth 1 -type d) ; do
        include_line="$(echo ${cur_include} | sed "s#./include/##")" 
        cp -a ./include/${include_line}/ %{buildroot}%{_datadir}/fusiondirectory/include/
      done
      
      # Files
      for cur_include in $(find ./include -mindepth 1 -maxdepth 1 -type f) ; do
        include_line="$(echo ${cur_include} | sed "s#./include/##")" 
        cp -a ./include/${include_line} %{buildroot}%{_datadir}/fusiondirectory/include/
      done
    fi
    
    
    # Locale section
    if [ -d ./locale ] ; then
      mkdir -p %{buildroot}%{_datadir}/fusiondirectory/locale/plugins/${cur_plugin}/locale/
      
      # Directories
      for cur_locale in $(find ./locale -mindepth 1 -maxdepth 1 -type d) ; do
        locale_line="$(echo ${cur_locale} | sed "s#./locale/##")" 
        cp -a ./locale/${locale_line} %{buildroot}%{_datadir}/fusiondirectory/locale/plugins/${cur_plugin}/locale/
      done
      
      # Files
      for cur_locale in $(find ./locale -mindepth 1 -maxdepth 1 -type f) ; do
        locale_line="$(echo ${cur_locale} | sed "s#./locale/##")" 
        cp -a ./locale/${locale_line} %{buildroot}%{_datadir}/fusiondirectory/locale/plugins/${cur_plugin}/locale/
      done
    fi

    
    # Personal section
    if [ -d ./personal ] ; then
      mkdir -p %{buildroot}%{_datadir}/fusiondirectory/plugins/personal/
    
      # Directories
      for cur_personal in $(find ./personal -mindepth 1 -maxdepth 1 -type d) ; do
        personal_line="$(echo ${cur_personal} | sed "s#./personal/##")" 
        cp -a ./personal/${personal_line} %{buildroot}%{_datadir}/fusiondirectory/plugins/personal/
      done
    
      # Files
      for cur_personal in $(find ./personal -mindepth 1 -maxdepth 1 -type f) ; do
        personal_line="$(echo ${cur_personal} | sed "s#./personal/##")" 
        cp -a ./personal/${personal_line} %{buildroot}%{_datadir}/fusiondirectory/plugins/personal/
      done
    fi
    
    # Contrib section for samba and supann
    if [ "${cur_plugin}" = "samba" ] ; then
      mkdir -p %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-samba/
      cp -a ./contrib/fix_munged %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-samba/
      
    elif [ "${cur_plugin}" = "supann" ] ; then
      mkdir -p %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-${cur_plugin}/examples/
      cp -a ./contrib/supann/* %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-${cur_plugin}/examples/
    fi 
    
    
    # Openldap section
    if [ -d ./contrib/openldap ] ; then
      mkdir -p %{buildroot}%{_sysconfdir}/openldap/schema/fusiondirectory/
      mkdir -p %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-${cur_plugin}-schema/
      cp ../../fusiondirectory-%{version}/{AUTHORS,Changelog,COPYING} %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-${cur_plugin}-schema/   
 
      # Directories
      for cur_openldap in $(find ./contrib/openldap -mindepth 1 -maxdepth 1 -type d) ; do
        openldap_line="$(echo ${cur_openldap} | sed "s#./contrib/openldap/##")" 
        cp -a ./contrib/openldap/${openldap_line} %{buildroot}%{_sysconfdir}/openldap/schema/fusiondirectory/
      done
    
      # Files
      for cur_openldap in $(find ./contrib/openldap -mindepth 1 -maxdepth 1 -type f ! -name 'example.ldif' ) ; do
        openldap_line="$(echo ${cur_openldap} | sed "s#./contrib/openldap/##")" 
        cp -a ./contrib/openldap/${openldap_line} %{buildroot}%{_sysconfdir}/openldap/schema/fusiondirectory/
      done
    fi
    
    
    # SQL section
    if [ -d ./contrib/sql ] ; then
      mkdir -p %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-${cur_plugin}-schema/
      cp ../../fusiondirectory-%{version}/{AUTHORS,Changelog,COPYING} %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-${cur_plugin}-schema/   
 
      # Directories
      for cur_sql in $(find ./contrib/sql -mindepth 1 -maxdepth 1 -type d) ; do
        sql_line="$(echo ${cur_sql} | sed "s#./contrib/sql/##")" 
        cp -a ./contrib/sql/${sql_line} %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-${cur_plugin}-schema/
      done
    
      # Files
      for cur_sql in $(find ./contrib/sql -mindepth 1 -maxdepth 1 -type f ! -name 'example.ldif' ) ; do
        sql_line="$(echo ${cur_sql} | sed "s#./contrib/sql/##")" 
        cp -a ./contrib/sql/${sql_line} %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-${cur_plugin}-schema/
      done   
    fi
  fi
 
    if [ -d ./contrib/docs ] ; then
      mkdir -p %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-${cur_plugin}/
      # Files
      for cur_docs in $(find ./contrib/docs -mindepth 1 -maxdepth 1 -type f) ; do
        docs_line="$(echo ${cur_docs} | sed "s#./contrib/docs/##")"
        cp -a ./contrib/docs/${docs_line} %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-${cur_plugin}/
      done
    fi
 

	# Docs
	mkdir -p %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-${cur_plugin}/
	cp ../../fusiondirectory-%{version}/{AUTHORS,Changelog,COPYING} %{buildroot}%{_datadir}/doc/fusiondirectory-plugin-${cur_plugin}/ 
 
	# Exiting plugin directory
	cd ..
done


%clean
rm -Rf %{buildroot}


%package addressbook
Group:		Applications/System
Summary:	Simple addressbook plugin
Requires:	fusiondirectory >= %{version}

%description addressbook
Simple addressbook plugin

%package alias
Group:		Applications/System
Summary:	Manage fonctional aliases
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-mail

%description alias
Manage fonctional aliases

%package apache2
Group:		Applications/System
Summary:	Apache2 vhost management
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description apache2
Apache2 vhost management

%package argonaut
Group:		Applications/System
Summary:	Communication layer between various software and the JSON-RPC Argonaut Server
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description argonaut
Communication layer between various software and the JSON-RPC Argonaut Server

%package asterisk
Group:		Applications/System
Summary:	Phone backend management with report functionality
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems,fusiondirectory-plugin-database-connector

%description asterisk
Phone backend management with report functionality

%package autofs
Group:		Applications/System
Summary:	Management of automount entries
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description autofs
Management of automount entries

%package cyrus
Group:		Applications/System
Summary:	Cyrus account management
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-mail

%description cyrus
Cyrus account management

%package dashboard
Group:		Applications/System
Summary:	Allows administrators to have several useful information
Requires:	fusiondirectory >= %{version}

%description dashboard
Allows administrators to have several useful information

%package debconf
Group:		Applications/System
Summary:	Management of debconf profile
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-argonaut

%description debconf
Management of debconf profile

%package developers
Group:		Applications/System
Summary:	Management plugin for developers
Requires:	fusiondirectory >= %{version}

%description developers
Management plugin for developers

%package dhcp
Group:		Applications/System
Summary:	DHCP service management
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description dhcp
DHCP service management

%package dns
Group:		Applications/System
Summary:	DNS service management
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description dns
DNS service management

%package dovecot
Group:		Applications/System
Summary:	Dovecot account management
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description dovecot
Dovecot account management

%package dsa
Group:		Applications/System
Summary:	Manage service security account in the LDAP
Requires:	fusiondirectory >= %{version}

%description dsa
Manage service security account in the LDAP

%package fai
Group:		Applications/System
Summary:	Linux system deployment management
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems,fusiondirectory-plugin-argonaut

%description fai
Linux system deployment management

%package fax
Group:		Applications/System
Summary:	Fax management backend with report functionality
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems,fusiondirectory-plugin-database-connector

%description fax
Fax management backend with report functionality

%package freeradius
Group:		Applications/System
Summary:	Manage users and groups for a freeradius server
Requires:	fusiondirectory >= %{version}

%description freeradius
Manage users and groups for a freeradius server

%package fusioninventory
Group:		Applications/System
Summary:	Fusioninventory inventory Management
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description fusioninventory
Fusioninventory inventory Management

%package game
Group:		Applications/System
Summary:	A tutorial plugin to discover FusionDirectory
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems,fusiondirectory-plugin-mail

%description game
A tutorial plugin to discover FusionDirectory

%package gpg
Group:		Applications/System
Summary:	Management plugin for gpg
Requires:	fusiondirectory >= %{version}

%description gpg
Management plugin for gpg

%package ipmi
Group:		Applications/System
Summary:	Basic ipmi support
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description ipmi
Basic ipmi support

%package kolab
Group:		Applications/System
Summary:	Kolab2 management
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-mail,fusiondirectory-plugin-cyrus

%description kolab
Kolab2 management

%package ldapdump
Group:		Applications/System
Summary:	Ldap raw visualisation
Requires:	fusiondirectory >= %{version}

%description ldapdump
Ldap raw visualisation

%package ldapmanager
Group:		Applications/System
Summary:	Simple LDAP backup and insertion tasks
Requires:	fusiondirectory >= %{version},openldap-clients

%description ldapmanager
Simple LDAP backup and insertion tasks

%package mail
Group:		Applications/System
Summary:	Mail management base
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description mail
Mail management base

%package nagios
Group:		Applications/System
Summary:	Nagios account settings management
Requires:	fusiondirectory >= %{version}

%description nagios
Nagios account settings management

%package netgroups
Group:		Applications/System
Summary:	Nis Netgroups account management
Requires:	fusiondirectory >= %{version}

%description netgroups
Nis Netgroups account management

%package openstack-compute
Group:		Applications/System
Summary:	Create users in Nova
Requires:	fusiondirectory >= %{version}

%description openstack-compute
Create users in Nova

%package opsi
Group:		Applications/System
Summary:	Opsi deployment management for Windows clients
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems,fusiondirectory-plugin-dns,fusiondirectory-plugin-samba

%description opsi
Opsi deployment management for Windows clients

%package puppet
Group:		Applications/System
Summary:	Manage a puppet server
Requires:	fusiondirectory >= %{version}

%description puppet
Manage a puppet server

%package pureftpd
Group:		Applications/System
Summary:	PureFTPD connectivity plugin
Requires:	fusiondirectory >= %{version}

%description pureftpd
PureFTPD connectivity plugin

%package quota
Group:		Applications/System
Summary:	Plugin for storing filesystem quota per user inside LDAP tree
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description quota
Plugin for storing filesystem quota per user inside LDAP tree

%package repository
Group:		Applications/System
Summary:	Plugin to manage repository for build systems
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description repository
Plugin to manage repository for build systems

%package rsyslog
Group:		Applications/System
Summary:	Rsyslog logging plugin
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems,fusiondirectory-plugin-database-connector

%description rsyslog
Rsyslog logging plugin

%package samba
Group:		Applications/System
Summary:	Samba 3 integration
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description samba
Samba 3 integration

%package sogo
Group:		Applications/System
Summary:	SOgo Account Management
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description sogo
SOgo Account Management

%package squid
Group:		Applications/System
Summary:	Squid connectivity plugin
Requires:	fusiondirectory >= %{version}

%description squid
Squid connectivity plugin

%package ssh
Group:		Applications/System
Summary:	SSH key plugin
Requires:	fusiondirectory >= %{version}

%description ssh
SSH key plugin

%package sudo
Group:		Applications/System
Summary:	Sudo manager
Requires:	fusiondirectory >= %{version}

%description sudo
Sudo manager

%package supann
Group:		Applications/System
Summary:	This Plugin aims to provide a full LDAP interface to SUPANN schema
Requires:	fusiondirectory >= %{version}

%description supann
This Plugin aims to provide a full LDAP interface to SUPANN schema

%package sympa
Group:		Applications/System
Summary:	Management of alias list of sympa
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems,fusiondirectory-plugin-alias

%description sympa
Management of alias list of sympa

%package systems
Group:		Applications/System
Summary:	System management base plugin
Requires:	fusiondirectory >= %{version}

%description systems
System management base plugin

%package uw-imap
Group:		Applications/System
Summary:	UW imap mail method
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-mail

%description uw-imap
UW imap mail method

%package weblink
Group:		Applications/System
Summary:	Plugin to access remote management of systems
Requires:	fusiondirectory >= %{version},fusiondirectory-plugin-systems

%description weblink
Plugin to access remote management of systems

%package webservice
Group:		Applications/System
Summary:	Management plugin for webservice
Requires:	fusiondirectory >= %{version}

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




%package alias-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory alias plugin

%description alias-schema
LDAP schema for FusionDirectory alias plugin



%package apache2-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory apache2 plugin

%description apache2-schema
LDAP schema for FusionDirectory apache2 plugin



%package argonaut-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory argonaut plugin

%description argonaut-schema
LDAP schema for FusionDirectory argonaut plugin



%package asterisk-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory asterisk plugin

%description asterisk-schema
LDAP schema for FusionDirectory asterisk plugin



%package autofs-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory autofs plugin

%description autofs-schema
LDAP schema for FusionDirectory autofs plugin



%package cyrus-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory cyrus plugin

%description cyrus-schema
LDAP schema for FusionDirectory cyrus plugin



%package dashboard-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory dashboard plugin

%description dashboard-schema
LDAP schema for FusionDirectory dashboard plugin



%package debconf-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory debconf plugin

%description debconf-schema
LDAP schema for FusionDirectory debconf plugin



%package dhcp-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory dhcp plugin

%description dhcp-schema
LDAP schema for FusionDirectory dhcp plugin



%package dns-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory dns plugin

%description dns-schema
LDAP schema for FusionDirectory dns plugin



%package dovecot-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory dovecot plugin

%description dovecot-schema
LDAP schema for FusionDirectory dovecot plugin



%package dsa-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory dsa plugin

%description dsa-schema
LDAP schema for FusionDirectory dsa plugin



%package fai-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory fai plugin

%description fai-schema
LDAP schema for FusionDirectory fai plugin



%package fax-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory fax plugin

%description fax-schema
LDAP schema for FusionDirectory fax plugin



%package freeradius-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory freeradius plugin

%description freeradius-schema
LDAP schema for FusionDirectory freeradius plugin



%package fusioninventory-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory fusioninventory plugin

%description fusioninventory-schema
LDAP schema for FusionDirectory fusioninventory plugin



%package gpg-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory gpg plugin

%description gpg-schema
LDAP schema for FusionDirectory gpg plugin



%package ipmi-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory ipmi plugin

%description ipmi-schema
LDAP schema for FusionDirectory ipmi plugin



%package kolab-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory kolab plugin

%description kolab-schema
LDAP schema for FusionDirectory kolab plugin



%package mail-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory mail plugin

%description mail-schema
LDAP schema for FusionDirectory mail plugin



%package nagios-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory nagios plugin

%description nagios-schema
LDAP schema for FusionDirectory nagios plugin



%package netgroups-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory netgroups plugin

%description netgroups-schema
LDAP schema for FusionDirectory netgroups plugin



%package openstack-compute-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory openstack-compute plugin

%description openstack-compute-schema
LDAP schema for FusionDirectory openstack-compute plugin



%package opsi-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory opsi plugin

%description opsi-schema
LDAP schema for FusionDirectory opsi plugin



%package puppet-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory puppet plugin

%description puppet-schema
LDAP schema for FusionDirectory puppet plugin



%package pureftpd-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory pureftpd plugin

%description pureftpd-schema
LDAP schema for FusionDirectory pureftpd plugin



%package quota-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory quota plugin

%description quota-schema
LDAP schema for FusionDirectory quota plugin



%package repository-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory repository plugin

%description repository-schema
LDAP schema for FusionDirectory repository plugin



%package samba-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory samba plugin

%description samba-schema
LDAP schema for FusionDirectory samba plugin



%package sogo-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory sogo plugin

%description sogo-schema
LDAP schema for FusionDirectory sogo plugin



%package squid-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory squid plugin

%description squid-schema
LDAP schema for FusionDirectory squid plugin



%package ssh-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory ssh plugin

%description ssh-schema
LDAP schema for FusionDirectory ssh plugin



%package sudo-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory sudo plugin

%description sudo-schema
LDAP schema for FusionDirectory sudo plugin



%package supann-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory supann plugin

%description supann-schema
LDAP schema for FusionDirectory supann plugin



%package sympa-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory sympa plugin

%description sympa-schema
LDAP schema for FusionDirectory sympa plugin



%package systems-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory systems plugin

%description systems-schema
LDAP schema for FusionDirectory systems plugin



%package weblink-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory weblink plugin

%description weblink-schema
LDAP schema for FusionDirectory weblink plugin



%package webservice-schema
Group:		Applications/System
Summary:	LDAP schema for FusionDirectory webservice plugin

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



# Generated by script generate_post_plugins.sh
# This is the post_plugins.spec file
%post addressbook
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post alias
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post apache2
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post argonaut
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post asterisk
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post autofs
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post cyrus
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post dashboard
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


%post fax
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post freeradius
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post fusioninventory
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post game
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post gpg
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post ipmi
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post kolab
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


%post openstack-compute
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


%post rsyslog
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


%post uw-imap
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post weblink
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%post webservice
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%post applications
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%post ejbca
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales

%post personal
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


# Generated by script generate_postun_plugins.sh
# This is the postun_plugins.spec file
%postun addressbook
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun alias
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun apache2
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun argonaut
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun asterisk
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun autofs
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun cyrus
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun dashboard
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


%postun fax
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun freeradius
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun fusioninventory
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun game
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun gpg
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun ipmi
%{_sbindir}/fusiondirectory-setup --update-cache --update-locales


%postun kolab
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


%postun openstack-compute
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


%postun rsyslog
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


%postun uw-imap
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



%files addressbook
%defattr(0644,root,root)
# Addons section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/addressbook/address_edit.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/addressbook/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/addressbook/contents.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/addressbook/address_info.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/addressbook/dial.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/addressbook/class_addressbook.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/addressbook/remove.tpl
# HTML section
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/addressbook
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/addressbook/images
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/addressbook/getvcard.php
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/addressbook/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-addressbook/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-addressbook/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-addressbook/COPYING


%files alias
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/alias/class_aliasManagement.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/alias/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/alias/class_mailAliasDistribution.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/alias/class_mailAliasRedirection.inc
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/alias/class_aliasConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/alias/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/alias/images/iconMiniMailDistribution.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/alias/images/iconMiniSympa.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/alias/images/icon.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/alias/images/iconMiniMailredirection.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/alias/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-alias/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-alias/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-alias/COPYING


%files apache2
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/apache2/class_serviceApacheVhostEdit.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/apache2/serviceApacheVhostEdit-filter.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/apache2/serviceApacheVhostEdit-filter.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/apache2/remove.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/apache2/class_serviceApacheVhostManagement.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/apache2/serviceApacheVhostEdit-list.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/apache2/serviceApacheVhostEdit-list.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/apache2/serviceApacheVhostEditFooter.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/apache2/tabs_serviceApacheVhostEdit.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/apache2/class_serviceApacheVhost.inc
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/apache2/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-apache2/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-apache2/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-apache2/COPYING


%files argonaut
%defattr(0644,root,root)
# Addons section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/argonaut/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/argonaut/deploy-list.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/argonaut/class_argonautQueue.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/argonaut/argonaut_import_file.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/argonaut/class_filterArgonautEvents.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/argonaut/events/timestamp_select.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/argonaut/events/class_EventAddSystemDialog.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/argonaut/events/eventTargetSystems-filter.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/argonaut/events/eventTargetSystems-filter.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/argonaut/events/class_filterSystemByIp.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/argonaut/events/DaemonEvent.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/argonaut/events/target_list.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/argonaut/events/class_DaemonEvent.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/argonaut/events/eventTargetSystems-list.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/argonaut/class_argonautImportFile.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/argonaut/deploy-list.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/argonaut/remove.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/argonaut/deploy-filter.xml
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/argonaut/class_argonautDNSConfig.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/argonaut/class_argonautFuseConfig.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/argonaut/class_argonautMirrorConfig.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/argonaut/class_argonautFuseOPSIConfig.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/argonaut/class_argonautServer.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/argonaut/class_argonautFuseLTSPConfig.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/argonaut/class_argonautFuseFAIConfig.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/argonaut/class_argonautClient.inc
# HTML section
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/argonaut
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/argonaut/images
# Include section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/include/jsonRPCClient.php
%attr (-,root,root)	%{_datadir}/fusiondirectory/include/class_supportDaemon.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/include/simpleplugin/class_BootKernelAttribute.inc
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/argonaut/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-argonaut/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-argonaut/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-argonaut/COPYING


%files asterisk
%defattr(0644,root,root)
# Addons section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/fonreports/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/fonreports/contents.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/fonreports/class_fonreport.inc
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/asterisk/class_serviceAsterisk.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/asterisk/phone.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/asterisk/class_phoneGeneric.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/asterisk/phonesettings.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/asterisk/tabs_phone.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/macro/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/macro/parameter.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/macro/macro-filter.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/macro/class_gofonMacroManagement.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/macro/paste_generic.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/macro/class_gofonMacroParameters.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/macro/tabs_macros.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/macro/macro-filter.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/macro/generic.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/macro/remove.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/macro/macro-list.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/macro/class_gofonMacro.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/conference/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/conference/class_phoneConferenceManagment.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/conference/paste_generic.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/conference/class_phoneConferenceGeneric.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/conference/conf-filter.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/conference/generic.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/conference/remove.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/conference/conf-filter.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/conference/conf-list.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/conference/tabs_conference.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/ogroups/asterisk/phonequeue.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/ogroups/asterisk/class_phonequeue.inc
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/asterisk/class_asteriskPluginConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/asterisk/images/options.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/asterisk/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/asterisk/images/iconMiniMacros.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/asterisk/images/iconMacros.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/asterisk/images/iconReport.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/asterisk/images/hardware.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/asterisk/images/iconConference.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/asterisk/images/icon.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/asterisk/images/iconMiniConference.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/asterisk/images/sound.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/asterisk/locale/nl/fusiondirectory.po
# Personal section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/phoneaccount/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/phoneaccount/class_phoneAccount.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/phoneaccount/paste_generic.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/phoneaccount/generic.tpl
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-asterisk/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-asterisk/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-asterisk/COPYING


%files autofs
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/autofs/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/autofs/class_nisMap.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/autofs/class_nisObject.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/autofs/class_autofsManagement.inc
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/autofs/class_autofsConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/autofs/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/autofs/images/iconMiniNisMap.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/autofs/images/iconMiniNisObject.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/autofs/images/icon.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/autofs/images/folder-remote.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/autofs/images/folder.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/autofs
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/autofs/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/autofs/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/autofs/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/autofs/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/autofs/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/autofs/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/autofs/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/autofs/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/autofs/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/autofs/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/autofs/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/autofs/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/autofs/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/autofs/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/autofs/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/autofs/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/autofs/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-autofs/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-autofs/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-autofs/COPYING


%files cyrus
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/cyrus/class_serviceCyrus.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/cyrus/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/cyrus/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/cyrus/locale/nl/fusiondirectory.po
# Personal section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/mail/mail-methods/class_mail-methods-cyrus.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/mail/mail-methods/class_mail-methods-sendmail-cyrus.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/mail/mail-methods/sieve_script.tpl
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-cyrus/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-cyrus/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-cyrus/COPYING


%files dashboard
%defattr(0644,root,root)
# Addons section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/dashboard/users_accounts.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/dashboard/class_dashBoardUsers.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/dashboard/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/dashboard/contents.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/dashboard/systems_pcids.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/dashboard/tabs_dashBoard.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/dashboard/network_dhcp.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/dashboard/class_dashBoardSystems.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/dashboard/main_stats.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/dashboard/class_dashBoard.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/dashboard/users_stats.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/dashboard/systems_stats.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/dashboard/class_dashBoardNetwork.inc
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/dashboard/class_dashBoardConfig.inc
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dashboard/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dashboard/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dashboard/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dashboard/COPYING


%files debconf
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/debconf/class_debconfStartup.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/debconfProfile/debconfProfile-filter.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/debconfProfile/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/debconfProfile/class_debconfProfileManagement.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/debconfProfile/debconfProfile-filter.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/debconfProfile/class_debconfProfileGeneric.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/debconf/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/debconf/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/debconf/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-debconf/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-debconf/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-debconf/COPYING


%files developers
%defattr(0644,root,root)
%attr (-,root,root)	%{_datadir}/doc/fusiondirectory-developers/
%attr (-,root,root)	%{_datadir}/doc/fusiondirectory-developers/CODING
%attr (-,root,root)	%{_datadir}/doc/fusiondirectory-developers/Doxyfile
%attr (-,root,root)	%{_datadir}/doc/fusiondirectory-developers/FDStandard
%attr (-,root,root)	%{_datadir}/doc/fusiondirectory-developers/filter.xsd 
%attr (-,root,root)	%{_datadir}/doc/fusiondirectory-developers/list.xsd
%attr (-,root,root)	%{_datadir}/doc/fusiondirectory-developers/simple-plugin
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/debug-help
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/debug-help
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/debug-help/images
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-developers/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-developers/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-developers/COPYING


%files dhcp
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/class_dhcpPlugin.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/class_dhcpOption.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/dhcpNewSection.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/dhcp_network.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/dhcp_dnszone.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/dhcp_tsigkey.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/class_dhcpGroup.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/class_dhcpSubnet.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/class_dhcpNewSectionDialog.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/class_dhcpSharedNetwork.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/class_dhcpSubClass.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/class_dhcpService.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/dhcp_sharedNetwork.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/dhcp_host.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/dhcp_pool.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/class_dhcpHost.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/dhcp_advanced.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/dhcp_group.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/class_dhcpPool.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/class_dhcpTSigKey.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/class_dhcpClass.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/class_dhcpAdvanced.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/dhcp_subnet.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/class_serviceDHCP.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/class_dhcpDnsZone.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/dhcp_service.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/remove_dhcp.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/serviceDHCP.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dhcp/class_dhcpNetwork.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/dhcp/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/dhcp/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dhcp/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dhcp/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dhcp/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dhcp/COPYING


%files dns
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dns/serviceDNSeditZoneEntries.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dns/serviceDNS.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dns/serviceDNSeditZone.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dns/class_DNS.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dns/class_serviceDNSeditZone.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dns/class_serviceDNSeditZoneEntries.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dns/class_serviceDNS.inc
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/dns/class_dnsConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/dns/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/dns/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dns/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dns/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dns/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dns/COPYING


%files dovecot
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/dovecot/class_serviceDovecot.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/dovecot/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/dovecot/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dovecot/locale/nl/fusiondirectory.po
# Personal section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/mail/mail-methods/class_mail-methods-dovecot.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dovecot/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dovecot/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dovecot/COPYING


%files dsa
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/dsa/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/dsa/class_dsaManagement.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/dsa/class_simpleSecurityObject.inc
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/dsa/class_dsaConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/dsa/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/dsa/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/dsa/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dsa/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dsa/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dsa/COPYING


%files fai
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/repository/fai_repository.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/repository/class_serviceRepository.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/class_faiLogView.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/class_faiStartup.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiVariableEntry.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiProfile.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiTemplateEntry.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiHook.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/branch_selector.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiPackageConfiguration.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiPartitionTable.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiGroupHandle.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/fai-filter.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiTemplateEdit.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiDiskEntry.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiPartitionTable.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiPartitionTableEntry.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiTemplateEdit.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiScriptEntry.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiManagement.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/classSelect/selectClass-list.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/classSelect/class_filterFAIClass.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/classSelect/selectClass-filter.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/classSelect/selectClass-filter.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/classSelect/class_classSelect.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/classSelect/selectClass-list.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_askClassName.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/fai-list.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiPackageConfiguration.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiScript.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_debconfTemplate.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/fai-list.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiProfileEntry.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiHookEntry.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiTemplate.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiTemplateEntry.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiProfile.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiPartition.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_filterFAI.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/fai-filter.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_FAI.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/paste_generic.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiPackage.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiPartitionTableEntry.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiNewBranch.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiVariable.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiPartition.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiVariableEntry.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiPackage.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiHookEntry.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiHook.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/remove.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiDiskEntry.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiProfileEntry.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/remove_branch.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiVariable.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiScriptEntry.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/packageSelect/selectPackage-list.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/packageSelect/class_filterFAIPackages.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/packageSelect/selectPackage-filter.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/packageSelect/class_filterFAIcustoms.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/packageSelect/selectPackage-list.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/packageSelect/class_packageSelect.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/packageSelect/selectPackage-filter.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiGroupHandle.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/askClassName.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/faiTemplate.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/fai/class_faiScript.inc
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/fai/class_faiConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/fai_small.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/branch.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/fai_template.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/freeze_grey.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/freeze.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/fai_partitionTable.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/branch_small.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/fai_new_variable.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/fai_hook.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/branch_small_grey.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/fai_variable.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/fai_new_template.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/fai_script.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/icon.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/fai_new_packages.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/fai_new_script.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/fai_new_hook.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/fai_profile.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/iconMiniRepository.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/removal_mark.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/package_configure.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/fai_new_partitionTable.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/raid.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/fai_packages.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fai/images/fai_new_profile.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fai/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fai/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fai/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fai/COPYING


%files fax
%defattr(0644,root,root)
# Addons section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/faxreports/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/faxreports/contents.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/faxreports/class_faxreport.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/faxreports/detail.tpl
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/fax/class_serviceFax.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/blocklists/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/blocklists/class_blocklistGeneric.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/blocklists/class_blocklistManagement.inc
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/fax/class_faxConfig.inc
# HTML section
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fax
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fax/images
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fax/getfax.php
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fax/locale/nl/fusiondirectory.po
# Personal section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/faxaccount/class_gofaxAccount.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/faxaccount/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/faxaccount/locals.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/faxaccount/faxNumberSelect/faxNumberSelect-list.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/faxaccount/faxNumberSelect/faxNumberSelect-filter.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/faxaccount/faxNumberSelect/faxNumberSelect-filter.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/faxaccount/faxNumberSelect/faxNumberSelect-list.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/faxaccount/faxNumberSelect/class_faxNumberSelect.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/faxaccount/lists.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/faxaccount/paste_generic.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/faxaccount/generic.tpl
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fax/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fax/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fax/COPYING


%files freeradius
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/freeradius/class_freeradiusGroup.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/freeradius/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/freeradius/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/freeradius/locale/nl/fusiondirectory.po
# Personal section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/freeradius/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/freeradius/class_freeradiusAccount.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-freeradius/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-freeradius/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-freeradius/COPYING


%files fusioninventory
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/fusioninventory/class_fiInventory.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/fusioninventory/class_fiInventoryAgent.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/fusioninventory/inventory.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/inventory/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/inventory/class_inventoryManagement.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/inventory/inventory-list.xml
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/fusioninventory/class_fiConfig.inc
# HTML section
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/collect.php
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fusioninventory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fusioninventory/images
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/fusioninventory/inventory.css
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/fusioninventory/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fusioninventory/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fusioninventory/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fusioninventory/COPYING


%files game
%defattr(0644,root,root)
# Addons section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/game/game.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/game/class_Game.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/game/class_Mission.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/game/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/game/images/win.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/game/images/game_logo.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/game/images/icon.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/game/images/mission_complete.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/game/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-game/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-game/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-game/COPYING


%files gpg
%defattr(0644,root,root)
# Addons section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/gpg/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/gpg/class_pgpServerInfo.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/gpg/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/gpg/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/gpg/locale/nl/fusiondirectory.po
# Personal section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/gpg/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/gpg/class_gpgAccount.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/gpg/pgpKeySelect/pgpKeySelect-list.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/gpg/pgpKeySelect/class_pgpKeySelect.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/gpg/pgpKeySelect/pgpKeySelect-filter.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/gpg/pgpKeySelect/pgpKeySelect-list.xml
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-gpg/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-gpg/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-gpg/COPYING


%files ipmi
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/ipmi/class_ipmiClient.inc
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ipmi/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ipmi/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ipmi/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ipmi/COPYING


%files kolab
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/kolab/class_serviceKolab.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/ogroups/kolab/class_mailogroup.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/ogroups/kolab/mail.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/ogroups/kolab/paste_mail.tpl
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/kolab/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/kolab/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/kolab/locale/nl/fusiondirectory.po
# Personal section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/mail/kolab/class_mail-methods-kolab22.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/mail/kolab/class_mail-methods-kolab.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/kolab/class_kolabAccount.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/kolab/main.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-kolab/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-kolab/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-kolab/COPYING


%files ldapdump
%defattr(0644,root,root)
# Addons section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/ldapdump/class_ldapDump.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/ldapdump/ldapdump.tpl
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapdump/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ldapdump/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ldapdump/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ldapdump/COPYING


%files ldapmanager
%defattr(0644,root,root)
# Addons section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/ldapmanager/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/ldapmanager/class_csvimport.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/ldapmanager/tabs_ldif.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/ldapmanager/contentcsv.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/ldapmanager/class_ldapmanager.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/ldapmanager/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/ldapmanager/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ldapmanager/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ldapmanager/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ldapmanager/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ldapmanager/COPYING


%files mail
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/imap/class_serviceIMAP.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/virus/class_serviceAntiVirus.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/spam/class_serviceSpamAssassin.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/postfix/class_servicePostfix.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/groups/mail/class_groupMail.inc
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/mail/class_mailPluginConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/mail/images/sieve_add_new_top.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/mail/images/sieve_add_new_bottom.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/mail/images/sieve_add_test.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/mail/locale/nl/fusiondirectory.po
# Personal section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/mail/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/mail/mailAddressSelect/class_mailAddressSelect.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/mail/class_mail-methods.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/mail/class_mailAccount.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/personal/mail/class_sieve.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-mail/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-mail/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-mail/COPYING


%files nagios
%defattr(0644,root,root)
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/nagios/class_nagiosConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/nagios/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/nagios/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/nagios/locale/nl/fusiondirectory.po
# Personal section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/nagios/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/nagios/class_nagiosAccount.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/nagios/nagios.tpl
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-nagios/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-nagios/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-nagios/COPYING


%files netgroups
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/netgroups/class_netgroupSystem.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/netgroups/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/netgroups/class_netgroupManagement.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/netgroups/class_filterNetGroupLDAP.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/netgroups/memberNisnetgroupSelect/class_memberNisnetgroupSelect.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/netgroups/class_netgroup.inc
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/netgroups/class_netgroupConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/netgroups/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/netgroups/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/netgroups/locale/nl/fusiondirectory.po
# Personal section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/netgroups/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/netgroups/class_netgroupMembership.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-netgroups/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-netgroups/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-netgroups/COPYING


%files openstack-compute
%defattr(0644,root,root)
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/openstack-compute/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/openstack-compute/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/openstack-compute/locale/nl/fusiondirectory.po
# Personal section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/openstack-compute/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/openstack-compute/class_novaAccount.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-openstack-compute/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-openstack-compute/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-openstack-compute/COPYING


%files opsi
%defattr(0644,root,root)
# Addons section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/opsi/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/opsi/opsiimport.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/opsi/class_opsiImport.inc
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/opsi/class_serviceOPSI.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/opsi/class_opsiClient.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/opsi/class_opsiProfileManagement.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/opsi/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/opsi/class_opsiProfile.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/opsi/class_opsiProductProperties.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/opsi/class_opsiSoftwareList.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/opsi/class_opsiOnDemandList.inc
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/opsi/class_opsiConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/opsi/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/opsi/images/iconSoftwareList.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/opsi/images/iconMiniSoftwareOnDemand.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/opsi/images/iconMiniSoftwareList.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/opsi/images/icon.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/opsi/images/iconSoftwareOnDemand.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/opsi/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-opsi/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-opsi/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-opsi/COPYING


%files puppet
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/puppet/class_servicePuppet.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/puppet/class_puppetNode.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/puppet/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/puppet/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/puppet/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-puppet/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-puppet/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-puppet/COPYING


%files pureftpd
%defattr(0644,root,root)
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/pureftpd/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/pureftpd/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/pureftpd/locale/nl/fusiondirectory.po
# Personal section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/pureftpd/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/pureftpd/class_pureftpdAccount.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-pureftpd/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-pureftpd/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-pureftpd/COPYING


%files quota
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/quota/service_quota_parameters.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/quota/class_serviceQuota.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/quota/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/quota/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/quota/locale/nl/fusiondirectory.po
# Personal section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/quota/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/quota/quota_section.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/quota/class_quotaAccount.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-quota/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-quota/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-quota/COPYING


%files repository
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/repository/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/repository/class_repositoryDistribution.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/repository/class_repositoryManagement.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/repository/class_repositorySection.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/repository/class_buildRepository.inc
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/repository/class_repositoryConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/repository/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/repository/images/icon.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/repository/images/iconSection.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/repository/images/iconDistribution.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/repository/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-repository/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-repository/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-repository/COPYING


%files rsyslog
%defattr(0644,root,root)
# Addons section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/rsyslog/rSyslog.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/rsyslog/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/rsyslog/rsyslogTabs.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/addons/rsyslog/class_rsyslog.inc
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/rsyslog/class_serviceSyslog.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/rsyslog/images/server.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/rsyslog/images/clock.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/rsyslog/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/rsyslog/images/workstation.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/rsyslog/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/rsyslog/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-rsyslog/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-rsyslog/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-rsyslog/COPYING


%files samba
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/samba/class_winstationGeneric.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/samba/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/samba/class_sambaDomainManagement.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/samba/class_sambaDomain.inc
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/samba/class_sambaPluginConfig.inc
%attr (-,root,root)	%{_datadir}/doc/fusiondirectory-plugin-samba/fix_munged
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/samba/locale/nl/fusiondirectory.po
# Personal section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/samba/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/samba/class_sambaMungedDial.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/samba/sambaLogonHours.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/samba/class_sambaAccount.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/samba/class_sambaLogonHours.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-samba/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-samba/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-samba/COPYING


%files sogo
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/sogo/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/sogo/class_sogoManagement.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/sogo/class_sogoResource.inc
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/sogo/class_sogoConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/sogo/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/sogo/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sogo/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sogo/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sogo/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sogo/COPYING


%files squid
%defattr(0644,root,root)
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/squid/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/squid/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/squid/locale/nl/fusiondirectory.po
# Personal section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/squid/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/squid/proxyAccount.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/squid/class_proxyAccount.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-squid/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-squid/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-squid/COPYING


%files ssh
%defattr(0644,root,root)
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/ssh/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/ssh/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/ssh/locale/nl/fusiondirectory.po
# Personal section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/ssh/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/ssh/class_sshAccount.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ssh/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ssh/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ssh/COPYING


%files sudo
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/sudo/usedoptions_section.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/sudo/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/sudo/class_sudoGeneric.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/sudo/class_sudoOption.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/sudo/tabs_sudo.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/sudo/class_sudoManagement.inc
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/sudo/class_sudoConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/sudo/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/sudo/images/negate.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/sudo/images/select_workstation.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/sudo/images/iconMiniDefault.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/sudo/images/icon.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/sudo/images/iconMiniRole.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sudo/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sudo/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sudo/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sudo/COPYING


%files supann
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/supannStructures/class_supannStructuresManagement.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/supannStructures/class_entite.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/supannStructures/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/supannStructures/class_etablissement.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/supannStructures/class_supann.inc
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/supann/class_supannConfig.inc
# Files contrib supann
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/corps
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/eturegimeinscription_SISE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/discipline_EXAMPLE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/entite
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/etuelementpedagogique_EXAMPLE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/diplome_SISE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/etablissement_SUPANN
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/role
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/etuetape_EXAMPLE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/activite_CNU
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/diplome_EXAMPLE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/activite_REFERENS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/affiliation
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/typediplome_EXAMPLE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/eturegimeinscription_EXAMPLE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/typediplome_SISE
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/examples/discipline_SISE
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/supann/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/supann/images/iconMiniEntite.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/supann/images/profil.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/supann/images/user-student.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/supann/images/affiliation.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/supann/images/user-employee.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/supann/images/icon.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/supann/images/user-enrolee.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/supann/images/iconMiniEtablissement.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/supann/locale/nl/fusiondirectory.po
# Personal section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/supann/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/supann/student_subscription.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/supann/class_supannAccount.inc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann/COPYING


%files sympa
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/sympa/class_serviceSympa.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/sympa/class_sympaAlias.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/sympa/images/iconMini.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/sympa/images/icon.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/sympa/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sympa/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sympa/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sympa/COPYING


%files systems
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/serverService-filter.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/printer.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/tabs_workstation.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/class_componentGeneric.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/main.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/class_systemManagement.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/class_systemImport.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/SelectDeviceType.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/class_terminalStartup.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/class_serverGeneric.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/tabs_terminal.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/serverService-list.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/system-filter.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/class_serverService.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/terminal/class_serviceTerminal.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/ServiceAddDialog.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/shares/service_share.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/shares/class_serviceShare.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/ntp/class_serviceNTP.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/class_ServiceAddDialog.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/ldap/class_serviceLDAP.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/class_goService.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/cups/serviceCUPS.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/services/cups/class_serviceCUPS.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/gencd.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/server_import.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/tabs_printers.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/serverService-filter.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/network.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/class_mobilePhoneGeneric.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/gencd_frame.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/class_terminalGeneric.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/system-list.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/class_printGeneric.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/class_filterServerService.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/serverService-list.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/tabs_component.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/class_SelectDeviceType.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/remove.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/class_workstationGeneric.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/phoneSelect/class_phoneSelect.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/phoneSelect/phoneSelect-filter.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/phoneSelect/phoneSelect-filter.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/phoneSelect/phoneSelect-list.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/phoneSelect/phoneSelect-list.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/ppd/remove_ppd.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/ppd/class_printerPPDSelectionDialog.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/ppd/printerPPDDialog.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/ppd/class_printerPPDDialog.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/ppd/class_ppdManager.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/ppd/printerPPDSelectionDialog.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/tabs_server.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/class_networkSettings.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/network_section.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/class_filterSYSTEMS.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/system-filter.xml
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/password.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/ogroups/goto/termgroup.tpl
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/ogroups/goto/class_termgroup.inc
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/systems/class_systemsPluginConfig.inc
# HTML section
# Directories
# Files in the directory
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/clock.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/server_error.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/select_default.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/service_imap.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/branch.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/select_newsystem.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/server_busy.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/prio_decrease.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/drives.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/prio_increase.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/freeze.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/terminal_locked.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/localboot.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/iconMiniHotPlugDevices.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/status_restarting.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/select_new_terminal.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/reinstall.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/scanner.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/service_apache.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/edit_share.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/sysinfo.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/status_start_all.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/keyboard.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/workstation_locked.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/rescan.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/service_ldap.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/workstation_error.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/status_stop.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/list_reset_password.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/terminal_error.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/status_start.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/list_new_app.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/server_locked.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/display.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/logon_script.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/hotplug.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/status_stop_all.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/hardware.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/view_logs.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/iconHotplugDevices.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/mouse.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/select_new_server.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/kiosk.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/workstation_busy.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/service_print.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/fai_settings.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/status_pause.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/notify.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/memcheck.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/select_new_workstation.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/service_file.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/status_restart_all.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/service_terminal.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/select_device.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/list_new_device.png
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/plugins/systems/images/service_ntp.png
# Files
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/systems/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-systems/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-systems/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-systems/COPYING


%files uw-imap
%defattr(0644,root,root)
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/uw-imap/locale/nl/fusiondirectory.po
# Personal section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/mail/uw-imap/class_mail-methods-uwimap.inc
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/personal/mail/uw-imap/procmail_script.tpl
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-uw-imap/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-uw-imap/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-uw-imap/COPYING


%files weblink
%defattr(0644,root,root)
# Admin section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/admin/systems/weblink/class_webLink.inc
# Locale section
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/id/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/ca/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/zh/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/nb/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/ug/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/es/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/fr/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/ru/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/lv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/de/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/it/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/pl/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/es_VE/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/sv/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/pt/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/ar/fusiondirectory.po
%attr (-,root,root)	%{_datadir}/fusiondirectory/locale/plugins/weblink/locale/nl/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-weblink/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-weblink/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-weblink/COPYING


%files webservice
%defattr(0644,root,root)
# Config section
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/plugins/config/class_webserviceConfig.inc
# HTML section
# Directories
# Files
%attr (-,root,root)	%{_datadir}/fusiondirectory/html/jsonrpc.php
# Locale section
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/en/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/ar/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/ca/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/de/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/es/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/es_VE/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/fr/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/id/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/it/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/lv/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/nb/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/nl/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/pl/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/pt/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/ru/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/sv/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/ug/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/webservice/locale/zh/fusiondirectory.po
# Include section
%attr (-,root,root)     %{_datadir}/fusiondirectory/include/jsonrpcphp/jsonRPCServer.php
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-webservice/jsonrpc.php.doc
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-webservice/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-webservice/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-webservice/COPYING

%files ejbca
%defattr(0644,root,root)
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/en/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/ejbca/class_ejbcaCertificate.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/ejbca/class_ejbcaManagement.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/ejbca/main.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/ejbca/class_ejbcaCertSelect.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/ejbca/class_ejbcaCertificates.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/config/ejbca/class_ejbcaConfig.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/plugins/ejbca/themes/default/icons/16/apps/ejbca.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/plugins/ejbca/themes/default/icons/48/apps/ejbca.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/ar/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/ca/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/de/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/es/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/es_VE/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/fr/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/id/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/it/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/lv/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/nb/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/nl/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/pl/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/pt/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/ru/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/sv/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/ug/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/ejbca/locale/zh/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ejbca/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ejbca/COPYING
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ejbca/Changelog

%files applications
%defattr(0644,root,root)
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/applications/class_applicationGeneric.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/applications/class_applicationManagement.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/applications/class_webApplication.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/applications/main.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/admin/roles/class_applicationRights.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/config/applications/class_applicationsPluginConfig.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/html/plugins/applications/images/default_icon.png
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/ca/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/de/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/en/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/es/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/es_VE/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/fr/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/id/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/it/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/nb/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/nl/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/pl/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/pt/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/ru/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/ug/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/zh/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/ar/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/lv/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/applications/locale/sv/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-applications/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-applications/COPYING
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-applications/Changelog

%files personal
%defattr(0644,root,root)
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/personal/personal/class_personalInfo.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/personal/personal/class_socialHandlers.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/plugins/personal/personal/main.inc
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/ar/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/ca/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/cs_CZ/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/de/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/en/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/es/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/es_VE/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/fa_IR/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/fr/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/id/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/it/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/lv/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/nb/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/nl/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/pl/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/pt/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/pt_BR/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/ru/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/ru@petr1708/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/sv/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/ug/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/vi_VN/fusiondirectory.po
%attr (-,root,root)     %{_datadir}/fusiondirectory/locale/plugins/personal/locale/zh/fusiondirectory.po
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-personal/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-personal/COPYING
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-personal/Changelog



%files alias-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/alias-fd-conf.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/alias-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-alias-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-alias-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-alias-schema/COPYING


%files apache2-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/mod_vhost_ldap.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-apache2-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-apache2-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-apache2-schema/COPYING


%files argonaut-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/argonaut-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-argonaut-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-argonaut-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-argonaut-schema/COPYING


%files asterisk-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/asterisk-fd-conf.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/asterisk-fd.schema
# Files
%attr (-,root,root)	%{_datadir}/doc/fusiondirectory-plugin-asterisk-schema/asteriskcdrdb.sql
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-asterisk-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-asterisk-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-asterisk-schema/COPYING


%files autofs-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/autofs-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-autofs-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-autofs-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-autofs-schema/COPYING


%files cyrus-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/cyrus-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-cyrus-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-cyrus-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-cyrus-schema/COPYING


%files dashboard-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/dashboard-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dashboard-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dashboard-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dashboard-schema/COPYING


%files debconf-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/debconf.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/debconf-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-debconf-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-debconf-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-debconf-schema/COPYING


%files dhcp-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/dhcp-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dhcp-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dhcp-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dhcp-schema/COPYING


%files dns-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/dns-fd-conf.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/dnszone.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dns-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dns-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dns-schema/COPYING


%files dovecot-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/dovecot-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dovecot-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dovecot-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dovecot-schema/COPYING


%files dsa-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/dsa-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dsa-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dsa-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-dsa-schema/COPYING


%files fai-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/fai.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/fai-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fai-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fai-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fai-schema/COPYING


%files fax-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/fax-fd.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/fax-fd-conf.schema
# Files
%attr (-,root,root)	%{_datadir}/doc/fusiondirectory-plugin-fax-schema/gofax.sql
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fax-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fax-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fax-schema/COPYING


%files freeradius-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/freeradius.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-freeradius-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-freeradius-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-freeradius-schema/COPYING


%files fusioninventory-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/inventory-fd.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/fusioninventory-fd.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/fusioninventory-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fusioninventory-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fusioninventory-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-fusioninventory-schema/COPYING


%files gpg-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/pgp-recon.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/pgp-keyserver.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/pgp-remte-prefs.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/gpg-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-gpg-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-gpg-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-gpg-schema/COPYING


%files ipmi-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/ipmi-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ipmi-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ipmi-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ipmi-schema/COPYING


%files kolab-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/rfc2739.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/kolab2.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-kolab-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-kolab-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-kolab-schema/COPYING


%files mail-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/mail-fd-conf.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/mail-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-mail-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-mail-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-mail-schema/COPYING


%files nagios-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/nagios-fd-conf.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/netways.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-nagios-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-nagios-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-nagios-schema/COPYING


%files netgroups-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/netgroups-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-netgroups-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-netgroups-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-netgroups-schema/COPYING


%files openstack-compute-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/nova_openldap.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-openstack-compute-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-openstack-compute-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-openstack-compute-schema/COPYING


%files opsi-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/opsi-fd.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/opsi-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-opsi-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-opsi-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-opsi-schema/COPYING


%files puppet-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/puppet.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/puppet-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-puppet-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-puppet-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-puppet-schema/COPYING


%files pureftpd-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/pureftpd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-pureftpd-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-pureftpd-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-pureftpd-schema/COPYING


%files quota-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/quota.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/quota-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-quota-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-quota-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-quota-schema/COPYING


%files repository-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/repository-fd.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/repository-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-repository-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-repository-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-repository-schema/COPYING


%files samba-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/samba-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-samba-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-samba-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-samba-schema/COPYING


%files sogo-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/sogo-fd-conf.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/calRessources.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/calEntry.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sogo-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sogo-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sogo-schema/COPYING


%files squid-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/proxy-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-squid-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-squid-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-squid-schema/COPYING


%files ssh-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/openssh-lpk.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ssh-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ssh-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ssh-schema/COPYING


%files sudo-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/sudo-fd-conf.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/sudo.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sudo-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sudo-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sudo-schema/COPYING


%files supann-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/internet2.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/supann_2009.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/supann-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-supann-schema/COPYING


%files sympa-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/sympa-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sympa-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sympa-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-sympa-schema/COPYING


%files systems-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/systems-fd-conf.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/systems-fd.schema
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/service-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-systems-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-systems-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-systems-schema/COPYING


%files weblink-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/weblink-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-weblink-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-weblink-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-weblink-schema/COPYING


%files webservice-schema
%defattr(0644,root,root)
# Files
%config(noreplace) %attr (-,root,root)	%{_sysconfdir}/openldap/schema/fusiondirectory/webservice-fd-conf.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-webservice-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-webservice-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-webservice-schema/COPYING

%files applications-schema
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/applications-fd-conf.schema
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/applications-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-applications-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-applications-schema/COPYING
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-applications-schema/Changelog

%files ejbca-schema
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/ejbca-fd-conf.schema
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/ejbca-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ejbca-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ejbca-schema/COPYING
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-ejbca-schema/Changelog

%files personal-schema
%attr (-,root,root)     %{_sysconfdir}/openldap/schema/fusiondirectory/personal-fd.schema
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-personal-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-personal-schema/COPYING
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-plugin-personal-schema/Changelog

########################

%changelog

* Tue Apr 1 2014 Jonathan SWAELENS <swaelens.jonathan@openmailbox.org> - 1.0.7.3-2.el6
- Add scriptaculous and prototype in the requires
- Add the patches for headers.tpl and password.tpl

* Mon Mar 31 2014 Jonathan SWAELENS <swaelens.jonathan@openmailbox.org> - 1.0.7.3-2.el6
- Adapt the scripts and patchs for the version 1.0.7.3

* Sun Jun 09 2013 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.6-2.el6
- Reorganize include directory files declaration in order to avoid multiple
  declaration in serveral RPMS (Closes #2504)
- Move the config/systems directory from sympa plugin to systems plugin (Closes #2423)
- Move the class_mailPluginConfig.inc file from core RPM to mail plugin (Closed #2485)
- Backport bugfix #2424 : Try to use PHP hash function if mhash is not available.
- Backport bugfix #2449 : Allow users with SAMBA attributes to be deleted properly.

* Sat May 12 2013 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.6-1.el6
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
- Remove obsolete plugins : php-gw 
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
* Sat Apr 17 2011 Olivier BONHOMME <obonhomme@nerim.net> - 1.0-1
- First Plugin integration
- Update packager identity
* Fri Apr 15 2011 Benoit Mortier <benoit.mortier@opensides.be> 
- First build of FusionDirectory 1.0 as an RPM, should work on SuSE and RedHat
