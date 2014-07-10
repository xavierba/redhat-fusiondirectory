Name:           php-Smarty3
Summary:        Template/Presentation Framework for PHP
Version:        _VERSION_
Release:        _SUB-VERSION_%{?dist}

Source0:        http://www.smarty.net/files/Smarty-%{version}.tar.gz
URL:            http://www.smarty.net
License:        LGPLv2+
Group:          Development/Libraries

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       php >= 5.2

%description
Although Smarty is known as a "Template Engine", it would be more accurately
described as a "Template/Presentation Framework." That is, it provides the
programmer and template designer with a wealth of tools to automate tasks
commonly dealt with at the presentation layer of an application. I stress the
word Framework because Smarty is not a simple tag-replacing template engine.
Although it can be used for such a simple purpose, its focus is on quick and
painless development and deployment of your application, while maintaining
high-performance, scalability, security and future growth.


%prep
%setup -qn Smarty-%{version}
#iconv -f iso8859-1 -t utf-8 NEWS > NEWS.conv && mv -f NEWS.conv NEWS
iconv -f iso8859-1 -t utf-8 change_log.txt > change_log.txt.conv && mv -f change_log.txt.conv change_log.txt


%build
# empty build section, nothing required


%install
rm -rf $RPM_BUILD_ROOT

# install smarty libs
install -d $RPM_BUILD_ROOT%{_datadir}/php/Smarty3
cp -a libs/* $RPM_BUILD_ROOT%{_datadir}/php/Smarty3/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc change_log.txt COPYING.lib demo README SMARTY_*.txt
%{_datadir}/php/Smarty3


%changelog
* Thu Apr 10 2014 Swaelens Jonathan <swaelens.jonathan@openmailbox.org> - 3.1.18-1
- Update to the version 3.1.18
* Sun Oct 06 2013 Benoit Mortier <benoit.mortier@opensides.be> - 3.1.15-1
- Initial Import
