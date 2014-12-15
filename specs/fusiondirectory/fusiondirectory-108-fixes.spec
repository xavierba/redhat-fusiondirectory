# This is the header.spec file
Name:       fusiondirectory
Version:    _VERSION_
Release:    _RELEASE_ 
Summary:    Web Based LDAP Administration Program

Group:      Applications/System
License:    GPLv2
URL:        http://www.%{name}.org

Buildarch:  noarch
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.te
Source2:    %{name}.fc

Patch0:     %{name}-fix_install-location-apache.patch
Patch1:     %{name}-fix_install-location.patch
Patch2:     %{name}-fix_libs-location.patch
Patch3:     %{name}-fix_openldap-schema-location.patch
Patch4:     %{name}-fix_pear-location.patch
Patch5:     %{name}-fix_prototype-location.patch
Patch6:     %{name}-fix_smarty3-location.patch


Requires:   php >= 5.3, php-ldap >= 5.3, php-imap >= 5.3, php-mbstring >= 5.3, php-pecl-imagick, php-fpdf

Requires:   perl-Path-Class, perl-Crypt-PasswdMD5, perl-File-Copy-Recursive, perl-Archive-Extract, perl-XML-Twig
Requires:   perl-Crypt-CBC, perl-LDAP, perl

Requires:   httpd, gettext, perl-ExtUtils-MakeMaker, prototype, prototype-httpd, scriptaculous, scriptaculous-httpd

Requires:   php-Smarty3, php-Smarty3-i18n, schema2ldif

%description 
FusionDirectory is a combination of system-administrator and end-user web
interface, designed to handle LDAP based setups.
Provided is access to posix, shadow, samba, proxy, fax, and Kerberos
accounts. It is able to manage the Postfix/Cyrus server combination
and can write user adapted sieve scripts.


# This is the package.spec file
%package schema
Group:			Applications/System
Summary:		Schema Definitions for the %{name} package
Requires:		openldap-clients

%description schema
Contains the Schema definition files for the %{name} admin package.


%package plugin-database-connector
Group:			Applications/System
Summary:		Database management framework for %{name}
Requires:		%{name} >= %{version}, php-pear-MDB2

%description plugin-database-connector
This package contains a database framework which allows connecting
%{name} to a database for storing specific datas. (Used only by specific
plugins)

############################
# SELINUX PACKAGE
############################

%package selinux
Group:			Applications/System
Summary:		SELinux policy for Fusiondirectory
Requires:		selinux-policy >= %{selinux_policyver}
Requires:		%{name} = %{version}-%{release}
BuildRequires:		checkpolicy, selinux-policy-devel, /usr/share/selinux/devel/policyhelp

%description selinux
This package contains the binary modules and sources files of the
SEPolicy needed for Fusiondirectory.

############################

%global webconfdir        %{_sysconfdir}/httpd/conf.d/
%global docdir            %{_datadir}/doc/
%global selinux_policyver %(%{__sed} -e 's,.*selinux-policy-\\([^/]*\\)/.*,\\1,' /usr/share/selinux/devel/policyhelp || echo 0.0.0)

# SELinux policy variants
%global selinux_variants mls strict targeted

############################

# This is the prep.spec file
%prep

# Create build directory
%setup -c -q -n %{name}-%{version}

# Source FD-core
# Extract Source
%setup -T -D -b 0 

# Apply all the patches
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

############################
# SELINUX PREP
############################

# SELinux build environment setup
mkdir SELinux
cp -p %{SOURCE1} %{SOURCE2} SELinux

# Change version of %{name}.te
sed -i 's/_SELINUX-VERSION_/%{version}/g' SELinux/%{name}.te

############################
# SELINUX BUILD
############################

%build
# Build SELinux binary policy module
cd SELinux
for selinuxvariant in %{selinux_variants}
do
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
  mv %{name}.pp %{name}.pp.${selinuxvariant}
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
done
cd -

############################

# This is the install.spec file
%install
# Installation of FD-core
# Create %{buildroot}%{_datadir}/%{name}/
mkdir -p %{buildroot}%{_datadir}/%{name}

DIRS="ihtml plugins html include locale setup"
for i in $DIRS ; do
  cp -ua $i %{buildroot}%{_datadir}/%{name}
done

# Create spool and cache directories 
install -d -m 0770 %{buildroot}/var/spool/%{name}/
install -d -m 0770 %{buildroot}/var/cache/%{name}/{tmp,fai}/

# Create other directories
mkdir -p %{buildroot}%{_datadir}/man/man1/
mkdir -p %{buildroot}%{_datadir}/man/man5/
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/openldap/schema/%{name}/
mkdir -p %{buildroot}%{_datadir}/php/Smarty3/plugins/

# Set the rights
chmod 750 contrib/bin/*

# Prepare the man pages
gzip contrib/man/%{name}.conf.5
gzip contrib/man/%{name}-setup.1
gzip contrib/man/%{name}-insert-schema.1

# Move man files
cp contrib/man/%{name}-setup.1.gz %{buildroot}%{_datadir}/man/man1
cp contrib/man/%{name}-insert-schema.1.gz %{buildroot}%{_datadir}/man/man1
cp contrib/man/%{name}.conf.5.gz %{buildroot}%{_datadir}/man/man5

# Copy docs
mkdir -p %{buildroot}%{_datadir}/doc/{%{name},%{name}-plugin-database-connector,%{name}-schema}
cp ./AUTHORS ./Changelog ./COPYING %{buildroot}%{_datadir}/doc/%{name}/
cp ./AUTHORS ./Changelog ./COPYING %{buildroot}%{_datadir}/doc/%{name}-plugin-database-connector/
cp ./AUTHORS ./Changelog ./COPYING %{buildroot}%{_datadir}/doc/%{name}-schema/
cp contrib/%{name}.conf %{buildroot}%{_datadir}/doc/%{name}/

# Move smarty functions and create php lib directory if it exist
cp contrib/smarty/plugins/function.msgPool.php %{buildroot}%{_datadir}/php/Smarty3/plugins/function.msgPool.php
cp contrib/smarty/plugins/function.filePath.php %{buildroot}%{_datadir}/php/Smarty3/plugins/function.filePath.php
cp contrib/smarty/plugins/block.render.php %{buildroot}%{_datadir}/php/Smarty3/plugins/block.render.php

# Move the schemas
cp -a contrib/openldap/* %{buildroot}%{_sysconfdir}/openldap/schema/%{name}/
mkdir -p %{buildroot}%{_datadir}/doc/%{name}/
mv %{buildroot}%{_sysconfdir}/openldap/schema/%{name}/slapd.conf %{buildroot}%{_datadir}/doc/%{name}/slapd.conf-example

# Move executables
cp contrib/bin/* %{buildroot}%{_sbindir}

# Move apache configuration
cp contrib/apache/%{name}-apache.conf %{buildroot}%{_sysconfdir}/%{name}/

############################
# SELINUX INSTALL
############################

# Install SELinux Policy Module
for selinuxvariant in %{selinux_variants}
do
  install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
  install -p -m 644 SELinux/%{name}.pp.${selinuxvariant} \
    %{buildroot}%{_datadir}/selinux/${selinuxvariant}/%{name}.pp
done

############################


%clean
rm -Rf %{buildroot}


%post plugin-database-connector
%{_sbindir}/%{name}-setup --yes --check-directories --update-locales --update-cache

############################
# POST / POSTUN SELINUX
############################

%post selinux
# SELinux post and postun scriptlets
for selinuxvariant in %{selinux_variants}
do
  /usr/sbin/semodule -s ${selinuxvariant} -i \
    %{_datadir}/selinux/${selinuxvariant}/%{name}.pp &> /dev/null || :
done

  # Apply context for spool and cache directroy considering the %{name} policy
  /sbin/restorecon -R /var/spool/%{name}
  /sbin/restorecon -R /var/cache/%{name}

%postun selinux
if [ $1 -eq 0 ] ; then
  for selinuxvariant in %{selinux_variants}
  do
    /usr/sbin/semodule -s ${selinuxvariant} -r %{name} &> /dev/null || :
  done

  # Apply context for spool and cache directroy without the %{name} policy
  /sbin/restorecon -R /var/spool/%{name}
  /sbin/restorecon -R /var/cache/%{name}

%post
if [ -d /etc/httpd/conf.d ]; then

  # Copy FusionDirectory configuration to conf.d directories
  if [ ! -L /etc/httpd/conf.d/fusiondirectory.conf ]; then

    # Remove old instances of this file
    if [ -f /etc/httpd/conf.d/fusiondirectory.conf ]; then
      echo "Found old fusiondirectory apache configuration in /etc/httpd/conf.d - moving it to fusiondirectory.conf.orig..."
      echo "Please check for changes in /etc/fusiondirectory/fusiondirectory-apache.conf if you modified this file!"
      mv /etc/httpd/conf.d/fusiondirectory.conf /etc/httpd/conf.d/fusiondirectory.conf.orig
    fi

    echo "Making /fusiondirectory available in /etc/httpd/conf.d"

    # Add FusionDirectory include file
    ln -s /etc/fusiondirectory/fusiondirectory-apache.conf /etc/httpd/conf.d/fusiondirectory.conf
  fi

  service httpd reload
fi

# Remove old instances of this file
if [ -f /var/cache/fusiondirectory/template/fusiondirectory.conf ]; then
  #link the template to /var/cache/fusiondirectory/template from usr
  rm -f /var/cache/fusiondirectory/template/fusiondirectory.conf
  ln -s /usr/share/doc/fusiondirectory/fusiondirectory.conf  /var/cache/fusiondirectory/template/fusiondirectory.conf
else
  #link the configuration template to /var/cache/fusiondirectory/template from /usr/share/doc/fusiondirectory/
  ln -s /usr/share/doc/fusiondirectory/fusiondirectory.conf  /var/cache/fusiondirectory/template/fusiondirectory.conf
fi

%postun
if [ -d /etc/httpd/conf.d ]; then
  # Remove FusionDirectory include
  [ -L /etc/httpd/conf.d/fusiondirectory.conf ] && rm -f /etc/httpd/conf.d/fusiondirectory.conf

  # Restart servers
  if [ -x /usr/sbin/httpd ]; then
    service httpd restart
  fi
fi

%files
%defattr(-,root,root,-)
%{_mandir}/man1/%{name}-setup.1.gz
%{_mandir}/man5/%{name}.conf.5.gz

%{_datadir}/doc/%{name}/AUTHORS
%{_datadir}/doc/%{name}/COPYING
%{_datadir}/doc/%{name}/Changelog

%{_sbindir}/%{name}-setup
%{_datadir}/%{name}/html/images
%{_datadir}/%{name}/html/plugins
%{_datadir}/%{name}/html/themes
%{_datadir}/%{name}/html/*.php
%{_datadir}/%{name}/html/*.inc
%{_datadir}/%{name}/html/*.ico
%{_datadir}/%{name}/html/*.txt
%{_datadir}/%{name}/html/include/datepicker.js
%{_datadir}/%{name}/html/include/%{name}.js
%{_datadir}/%{name}/html/include/pulldown.js
%{_datadir}/%{name}/html/include/pwdStrength.js
%{_datadir}/%{name}/ihtml
%{_datadir}/%{name}/include/exporter
%{_datadir}/%{name}/include/password-methods
%{_datadir}/%{name}/include/simpleplugin
%{_datadir}/%{name}/include/select
%{_datadir}/%{name}/include/accept-to-gettext.inc
%{_datadir}/%{name}/include/class_acl.inc
%{_datadir}/%{name}/include/class_baseSelector.inc
%{_datadir}/%{name}/include/class_certificate.inc
%{_datadir}/%{name}/include/class_config.inc
%{_datadir}/%{name}/include/class_CopyPasteHandler.inc
%{_datadir}/%{name}/include/class_departmentSortIterator.inc
%{_datadir}/%{name}/include/class_divSelectBox.inc
%{_datadir}/%{name}/include/class_filter.inc
%{_datadir}/%{name}/include/class_filterLDAP.inc
%{_datadir}/%{name}/include/class_IconTheme.inc
%{_datadir}/%{name}/include/class_ldap.inc
%{_datadir}/%{name}/include/class_ldapFilter.inc
%{_datadir}/%{name}/include/class_ldapMultiplexer.inc
%{_datadir}/%{name}/include/class_listing.inc
%{_datadir}/%{name}/include/class_listingSortIterator.inc
%{_datadir}/%{name}/include/class_log.inc
%{_datadir}/%{name}/include/class_management.inc
%{_datadir}/%{name}/include/class_msg_dialog.inc
%{_datadir}/%{name}/include/class_msgPool.inc
%{_datadir}/%{name}/include/class_objects.inc
%{_datadir}/%{name}/include/class_plugin.inc
%{_datadir}/%{name}/include/class_pluglist.inc
%{_datadir}/%{name}/include/class_smbHash.inc
%{_datadir}/%{name}/include/class_session.inc
%{_datadir}/%{name}/include/class_SnapShotDialog.inc
%{_datadir}/%{name}/include/class_SnapshotHandler.inc
%{_datadir}/%{name}/include/class_sortableListing.inc
%{_datadir}/%{name}/include/class_tabs.inc
%{_datadir}/%{name}/include/class_tests.inc
%{_datadir}/%{name}/include/class_timezone.inc
%{_datadir}/%{name}/include/class_userinfo.inc
%{_datadir}/%{name}/include/class_xml.inc
%{_datadir}/%{name}/include/functions_debug.inc
%{_datadir}/%{name}/include/functions.inc
%{_datadir}/%{name}/include/php_setup.inc
%{_datadir}/%{name}/include/variables_common.inc
%{_datadir}/%{name}/include/variables.inc
%{_datadir}/%{name}/locale
%{_datadir}/%{name}/plugins
%{_datadir}/%{name}/setup
%{_sysconfdir}/%{name}/%{name}-apache.conf
%{_datadir}/doc/%{name}/slapd.conf-example
%{_datadir}/doc/%{name}/%{name}.conf
%{_datadir}/php/Smarty3/plugins/block.render.php
%{_datadir}/php/Smarty3/plugins/function.msgPool.php
%{_datadir}/php/Smarty3/plugins/function.filePath.php

%files schema
%defattr(-,root,root,-)
%{_mandir}/man1/%{name}-insert-schema.1.gz

%{_datadir}/doc/%{name}-schema/AUTHORS
%{_datadir}/doc/%{name}-schema/COPYING
%{_datadir}/doc/%{name}-schema/Changelog

%{_sysconfdir}/openldap/schema/%{name}/core-fd.schema
%{_sysconfdir}/openldap/schema/%{name}/rfc2307bis.schema
%{_sysconfdir}/openldap/schema/%{name}/ldapns.schema
%{_sysconfdir}/openldap/schema/%{name}/samba.schema
%{_sysconfdir}/openldap/schema/%{name}/recovery-fd.schema
%{_sysconfdir}/openldap/schema/%{name}/core-fd-conf.schema
%{_sbindir}/%{name}-insert-schema

%files plugin-database-connector
%defattr(-,root,root,-)
%{_datadir}/doc/%{name}-plugin-database-connector/AUTHORS
%{_datadir}/doc/%{name}-plugin-database-connector/COPYING
%{_datadir}/doc/%{name}-plugin-database-connector/Changelog

%{_datadir}/%{name}/include/class_databaseManagement.inc

############################
# FILES SELINUX
############################

%files selinux
%defattr(-,root,root,0755)
%doc SELinux/%{name}.te
%doc SELinux/%{name}.fc
%{_datadir}/selinux/*/%{name}.pp

