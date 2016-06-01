Name:       fusiondirectory-user-reminder
Version:    _VERSION_
Release:    _RELEASE_ 
Summary:    User reminder script for the FusionDirectory

Group:      Applications/System
License:    GPLv2
URL:        http://www.fusiondirectory.org

Buildarch:  noarch
Source0:    fusiondirectory-plugins-%{version}.tar.gz

Requires:   perl-Digest-SHA, perl-Email-Mime, perl-Mail-Sender, perl-LDAP, perl-TermReadKey

%description 
This is the script to manage the user reminder fonctionality.

%prep

%setup -c -q -n fusiondirectory-user-reminder-%{version}
%setup -T -D -b 0 -n fusiondirectory-plugins-%{version}

%install
mkdir -p %{buildroot}/usr/sbin/
cp ./user-reminder/contrib/bin/* %{buildroot}/usr/bin/
chmod +x %{buildroot}/usr/sbin/*

mkdir -p %{buildroot}/usr/share/doc/fusiondirectory-user-reminder/
cp ./webservice/contrib/docs/* %{buildroot}/usr/share/doc/fusiondirectory-user-reminder/

%clean
rm -Rf %{buildroot}

%files
%defattr(0644,root,root)
%attr(0755,root,root) /usr/sbin/fusiondirectory-user-reminder

%changelog
* Wed Jun 01 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.13-1
- Package fusiondirectory-user-reminder script
