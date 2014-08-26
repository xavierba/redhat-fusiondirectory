# This is the header.spec file
Name:       fusiondirectory
Version:    _VERSION_
Release:    _RELEASE_
Summary:    Web Based LDAP Administration Program

Group:      Applications/System
License:    GPLv2
URL:        http://www.fusiondirectory.org

Buildarch:  noarch
Source0:    %{name}-%{version}.tar.gz
Source2:    %{name}.te
Source3:    %{name}.fc

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

Requires:   httpd, gettext, perl-ExtUtils-MakeMaker
Requires:   prototype, prototype-httpd, scriptaculous, scriptaculous-httpd

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
Group:                  Applications/System
Summary:                SELinux policy for Fusiondirectory
Requires:               selinux-policy >= %{selinux_policyver}
Requires:               %{name} = %{version}-%{release}
BuildRequires:          checkpolicy, selinux-policy-devel, /usr/share/selinux/devel/policyhelp

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
cp -p %{SOURCE2} %{SOURCE3} SELinux

# Change version of fusiondirectory.te
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
  mv fusiondirectory.pp fusiondirectory.pp.${selinuxvariant}
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
done
cd -

# This is the install.spec file
%install
# Installation of FD-core
# Create %{buildroot}%{_datadir}/fusiondirectory/
mkdir -p %{buildroot}%{_datadir}/%{name}

DIRS="ihtml plugins html include locale setup"
for i in $DIRS ; do
  cp -ua $i %{buildroot}%{_datadir}/%{name}
done

# Create spool and cache directories 
install -d -m 0770 %{buildroot}/var/spool/%{name}/
install -d -m 0770 %{buildroot}/var/cache/%{name}/{tmp,template,locale}/

# Create other directories
mkdir -p %{buildroot}%{_datadir}/man/man1/
mkdir -p %{buildroot}%{_datadir}/man/man5/
mkdir -p %{buildroot}%{webconfdir}
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
mkdir -p %{buildroot}%{docdir}{%{name},%{name}-plugin-database-connector,%{name}-schema}
cp ./AUTHORS ./Changelog ./COPYING %{buildroot}%{docdir}%{name}/
cp ./AUTHORS ./Changelog ./COPYING %{buildroot}%{docdir}%{name}-plugin-database-connector/
cp ./AUTHORS ./Changelog ./COPYING %{buildroot}%{docdir}%{name}-schema/

# Move smarty functions and create php lib directory if it exist
cp contrib/smarty/plugins/function.msgPool.php %{buildroot}%{_datadir}/php/Smarty3/plugins/function.msgPool.php
cp contrib/smarty/plugins/function.filePath.php %{buildroot}%{_datadir}/php/Smarty3/plugins/function.filePath.php
cp contrib/smarty/plugins/block.render.php %{buildroot}%{_datadir}/php/Smarty3/plugins/block.render.php

# Move fusiondirectory.conf in template
cp contrib/%{name}.conf %{buildroot}/var/cache/%{name}/template/

# Move the schemas
cp -a contrib/openldap/* %{buildroot}%{_sysconfdir}/openldap/schema/%{name}/
mkdir -p %{buildroot}%{docdir}%{name}/
mv %{buildroot}%{_sysconfdir}/openldap/schema/%{name}/slapd.conf %{buildroot}%{docdir}%{name}/slapd.conf-example

# Move executables
cp contrib/bin/* %{buildroot}%{_sbindir}

# Move apache configuration
cp contrib/apache/%{name}-apache.conf %{buildroot}%{webconfdir}

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


# This is the post_core.spec file
%post
%{_sbindir}/%{name}-setup --yes --check-directories --update-locales --update-cache

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

  # Apply context for spool and cache directroy considering the fusiondirectory policy
  /sbin/restorecon -R /var/spool/%{name}
  /sbin/restorecon -R /var/cache/%{name}

%postun selinux
if [ $1 -eq 0 ] ; then
  for selinuxvariant in %{selinux_variants}
  do
    /usr/sbin/semodule -s ${selinuxvariant} -r %{name} &> /dev/null || :
  done

  # Apply context for spool and cache directroy without the fusiondirectory policy
  /sbin/restorecon -R /var/spool/%{name}
  /sbin/restorecon -R /var/cache/%{name}

%files
%defattr(-,root,root,-)

# Core files
%doc %attr(-,root,root) %{_datadir}/doc/%{name}/AUTHORS 
%doc %attr(-,root,root) %{_datadir}/doc/%{name}/Changelog 
%doc %attr(-,root,root) %{_datadir}/doc/%{name}/COPYING
%attr(755,root,root) %{_sbindir}/%{name}-setup
%attr(0644,root,root) %{_mandir}/man1/*.1*
%attr(0644,root,root) %{_mandir}/man5/*.5*
%attr(-,root,root)%{_datadir}/%{name}/locale/
%attr(0770, root, apache) %{_localstatedir}/spool/%{name}
%dir %attr(0770, root, apache) %{_localstatedir}/cache/%{name}
%attr(0770, root, apache) %{_localstatedir}/cache/%{name}/tmp
%attr(- root, apache) %{_localstatedir}/cache/%{name}/template/
%attr(0770, root, apache) %{_localstatedir}/cache/%{name}/locale
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/httpd/conf.d/%{name}-apache.conf
%attr(-, root,root) %{_datadir}/doc/%{name}/slapd.conf-example

# Core files
%attr(-,root,root)%{_datadir}/%{name}/html/*.php
%attr(-,root,root)%{_datadir}/%{name}/html/*.inc
%attr(-,root,root)%{_datadir}/%{name}/html/*.ico
%attr(-,root,root)%{_datadir}/%{name}/html/*.txt
%attr(-, root,root) %{_datadir}/%{name}/html/images
%attr(-, root,root) %{_datadir}/%{name}/html/plugins
%attr(-, root,root) %{_datadir}/%{name}/html/themes
%attr(-, root,root) %{_datadir}/%{name}/html/include
%attr(-, root,root) %{_datadir}/%{name}/html/include/datepicker.js
%attr(-, root,root) %{_datadir}/%{name}/html/include/%{name}.js
%attr(-, root,root) %{_datadir}/%{name}/html/include/pulldown.js
%attr(-, root,root) %{_datadir}/%{name}/html/include/pwdStrength.js
%attr(-, root,root) %{_datadir}/%{name}/html/include/overlib.js 
%attr(-, root,root) %{_datadir}/%{name}/ihtml
%attr(-, root,root) %{_datadir}/%{name}/setup

# Include Files
%attr(-,root,root)%{_datadir}/%{name}/include/accept-to-gettext.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_CopyPasteHandler.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_SnapShotDialog.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_SnapshotHandler.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_acl.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_baseSelector.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_certificate.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_config.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_departmentSortIterator.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_divSelectBox.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_divlist.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_filter.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_filterLDAP.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_ldap.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_ldapMultiplexer.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_listing.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_listingSortIterator.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_log.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_management.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_msgPool.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_msg_dialog.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_objects.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_plugin.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_pluglist.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_session.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_smbHash.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_sortableListing.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_tabs.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_tests.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_timezone.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_userinfo.inc
%attr(-,root,root)%{_datadir}/%{name}/include/class_xml.inc
%attr(-,root,root)%{_datadir}/%{name}/include/exporter/class_PDF.php
%attr(-,root,root)%{_datadir}/%{name}/include/exporter/class_cvsExporter.inc
%attr(-,root,root)%{_datadir}/%{name}/include/exporter/class_pdfExporter.inc
%attr(-,root,root)%{_datadir}/%{name}/include/functions.inc
%attr(-,root,root)%{_datadir}/%{name}/include/functions_debug.inc
%attr(-,root,root)%{_datadir}/%{name}/include/password-methods/class_password-methods-clear.inc
%attr(-,root,root)%{_datadir}/%{name}/include/password-methods/class_password-methods-crypt.inc
%attr(-,root,root)%{_datadir}/%{name}/include/password-methods/class_password-methods-md5.inc
%attr(-,root,root)%{_datadir}/%{name}/include/password-methods/class_password-methods-sasl.inc
%attr(-,root,root)%{_datadir}/%{name}/include/password-methods/class_password-methods-sha.inc
%attr(-,root,root)%{_datadir}/%{name}/include/password-methods/class_password-methods-smd5.inc
%attr(-,root,root)%{_datadir}/%{name}/include/password-methods/class_password-methods-ssha.inc
%attr(-,root,root)%{_datadir}/%{name}/include/password-methods/class_password-methods.inc
%attr(-,root,root)%{_datadir}/%{name}/include/php_setup.inc
%attr(-,root,root)%{_datadir}/%{name}/include/simpleplugin/class_attribute.inc
%attr(-,root,root)%{_datadir}/%{name}/include/simpleplugin/class_dialogAttributes.inc
%attr(-,root,root)%{_datadir}/%{name}/include/simpleplugin/class_helpersAttribute.inc
%attr(-,root,root)%{_datadir}/%{name}/include/simpleplugin/class_multiPlugin.inc
%attr(-,root,root)%{_datadir}/%{name}/include/simpleplugin/class_simpleManagement.inc
%attr(-,root,root)%{_datadir}/%{name}/include/simpleplugin/class_simplePlugin.inc
%attr(-,root,root)%{_datadir}/%{name}/include/simpleplugin/class_simpleService.inc
%attr(-,root,root)%{_datadir}/%{name}/include/simpleplugin/class_simpleTabs.inc
%attr(-,root,root)%{_datadir}/%{name}/include/simpleplugin/simple-filter.xml
%attr(-,root,root)%{_datadir}/%{name}/include/simpleplugin/simple-list.xml
%attr(-,root,root)%{_datadir}/%{name}/include/variables.inc
%attr(-,root,root)%{_datadir}/%{name}/include/variables_common.inc

# Smarty Files
%attr(-, root,root) %{_datadir}/php/Smarty3/plugins/function.msgPool.php
%attr(-, root,root) %{_datadir}/php/Smarty3/plugins/function.filePath.php
%attr(-, root,root) %{_datadir}/php/Smarty3/plugins/block.render.php

# Base plugins files
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/acl/acl-filter.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/acl/acl-filter.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/acl/acl-list.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/acl/acl_role.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/acl/class_aclManagement.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/acl/class_aclRole.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/acl/class_filterACL.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/acl/main.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/acl/paste_role.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/acl/remove.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/acl/tabs_acl.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/acl/tabs_acl_role.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/class_countryGeneric.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/class_dcObject.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/class_department.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/class_departmentManagement.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/class_domain.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/class_localityGeneric.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/class_organizationGeneric.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/country.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/dcObject.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/dep-filter.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/dep-filter.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/dep_iframe.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/dep-list.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/dep_move_confirm.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/domain.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/generic.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/locality.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/main.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/organization.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/remove.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/departments/tabs_department.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/class_filterGroupLDAP.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/class_group.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/class_groupManagement.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/generic.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/group-filter.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/group-filter.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/group-list.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/group-list.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/main.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/paste_generic.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/remove.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/singleUserSelect/class_singleUserSelect.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/singleUserSelect/singleUser-filter.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/singleUserSelect/singleUser-filter.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/singleUserSelect/singleUser-list.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/singleUserSelect/singleUser-list.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/tabs_group.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/trust_machines.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/userGroupSelect/class_userGroupSelect.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/userGroupSelect/selectUserGroup-filter.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/userGroupSelect/selectUserGroup-filter.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/userGroupSelect/selectUserGroup-list.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/userGroupSelect/selectUserGroup-list.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/userSelect/class_userSelect.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/userSelect/user-filter.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/userSelect/user-filter.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/userSelect/user-list.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/groups/userSelect/user-list.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/ogroups/class_ogroup.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/ogroups/class_ogroupManagement.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/ogroups/generic.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/ogroups/main.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/ogroups/objectSelect/class_filterLDAPDepartmentBlacklist.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/ogroups/objectSelect/class_objectSelect.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/ogroups/objectSelect/selectObject-filter.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/ogroups/objectSelect/selectObject-filter.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/ogroups/objectSelect/selectObject-list.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/ogroups/objectSelect/selectObject-list.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/ogroups/ogroup-filter.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/ogroups/ogroup-filter.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/ogroups/ogroup-list.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/ogroups/ogroup_objects.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/ogroups/paste_generic.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/ogroups/remove.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/ogroups/tabs_ogroups.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/ogroups/trust_machines.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/users/class_userManagement.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/users/main.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/users/password.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/users/remove.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/users/tabs_user.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/users/template.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/users/templatize.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/users/user-filter.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/users/user-filter.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/admin/users/user-list.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/generic/references/class_reference.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/generic/references/contents.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/generic/welcome/main.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/generic/welcome/welcome.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/generic/changed.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/generic/class_user.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/generic/generic_certs.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/generic/generic_picture.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/generic/generic.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/generic/main.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/generic/nochange.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/generic/password.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/generic/paste_generic.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/password/changed.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/password/class_password.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/password/main.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/password/nochange.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/password/password.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/posix/class_posixAccount.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/posix/groupSelect/class_filterLDAPBlacklist.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/posix/groupSelect/class_groupSelect.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/posix/groupSelect/group-filter.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/posix/groupSelect/group-filter.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/posix/groupSelect/group-list.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/posix/groupSelect/group-list.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/posix/main.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/posix/trustSelect/class_trustSelect.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/posix/trustSelect/trust-filter.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/posix/trustSelect/trust-filter.xml
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/posix/trustSelect/trust-list.tpl
%attr(-,root,root)%{_datadir}/%{name}/plugins/personal/posix/trustSelect/trust-list.xml

# Core plugins config section
%attr(-,root,root)%{_datadir}/%{name}/plugins/config/class_configInLdap.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/config/class_mainPluginsConfig.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/config/class_pluginsConfigInLdap.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/config/main.inc
%attr(-,root,root)%{_datadir}/%{name}/plugins/config/tabs_configInLdap.inc

# Password Recovery Feature
%attr (-,root,root)	%{_datadir}/%{name}/plugins/admin/password/class_recoveryConfig.inc
%attr (-,root,root)	%{_datadir}/%{name}/plugins/admin/password/main.inc
%attr (-,root,root)	%{_datadir}/%{name}/plugins/admin/password/recoveryConfig.tpl


%files schema
%defattr(-,root,root,-)
%attr(755,root,root) %{_sbindir}/%{name}-insert-schema
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/openldap/schema/%{name}/update-from-1.0.6-to-1.0.7/update-core-fd-conf.ldif
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/openldap/schema/%{name}/core-fd-conf.schema
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/openldap/schema/%{name}/core-fd.schema
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/openldap/schema/%{name}/ldapns.schema
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/openldap/schema/%{name}/recovery-fd.schema
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/openldap/schema/%{name}/rfc2307bis.schema
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/openldap/schema/%{name}/samba.schema
%doc %attr(-,root,root) %{_datadir}/doc/%{name}-schema/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/%{name}-schema/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/%{name}-schema/COPYING


%files plugin-database-connector
%defattr(-,root,root,-)
%attr(0644,root,root) %{_datadir}/%{name}/include/class_databaseManagement.inc
%doc %attr(-,root,root) %{_datadir}/doc/%{name}-plugin-database-connector/AUTHORS
%doc %attr(-,root,root) %{_datadir}/doc/%{name}-plugin-database-connector/Changelog
%doc %attr(-,root,root) %{_datadir}/doc/%{name}-plugin-database-connector/COPYING

############################
# FILES SELINUX
############################

%files selinux
%defattr(-,root,root,0755)
%doc SELinux/fusiondirectory.te
%doc SELinux/fusiondirectory.fc
%{_datadir}/selinux/*/fusiondirectory.pp

########################

%changelog

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
