Name:		schema2ldif
Version:	_VERSION_
Release:	_SUB-VERSION_%{dist}
Summary:	Tool to convert schema into ldif format

Group:		Applications/System
License:	BSD
URL:		https://forge.fusiondirectory.org/projects/schema2ldif
Source0:	http://repos.fusiondirectory.org/sources/1.0/schema2ldif-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

%description
schema2ldif is a tool to convert files in ldap schema format to ldif. 
It support various schema format and export clean an well format schema	
in ldif format.

%prep
%setup -q -n schema2ldif-%{version}

%build

%install
# Clean buildroot before install
rm -rf %{buildroot} 

# Install the command line utility
install -d %{buildroot}%{_bindir}
install -p -m 0755 bin/schema2ldif %{buildroot}%{_bindir}/schema2ldif

#install the manpage
install -d %{buildroot}%{_mandir}/man1/
install -p -m 0644  man/schema2ldif.1 %{buildroot}%{_mandir}/man1/schema2ldif.1.gz

%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%doc README LICENSE
%{_bindir}/schema2ldif
%{_mandir}/man1/schema2ldif.1.gz

%changelog
* Mon Oct 10 2013 Benoit Mortier <benoit.mortier@opensides.be> - 1.0-1
- Initial Release

