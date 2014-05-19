Name:           fusiondirectory-release-jenkins-develop       
Version:        1.0 
Release:        1%{dist}
Summary:        RPM Packages for FusionDirectory Develop (Jenkins)

Group:          System Environment/Base 
License:        GPLv2
URL:            https://forge.fusiondirectory.org/projects/fdirectory-rpm
Source0:        RPM-GPG-KEY-FUSIONDIRECTORY-JENKINS
Source1:        fusiondirectory-jenkins-develop.repo	
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch

%description
This package contains the FusionDirectory repository.

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE0} .
install -pm 644 %{SOURCE1} .

%build


%install
rm -rf $RPM_BUILD_ROOT

#GPG Key
install -Dpm 644 %{SOURCE0} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-FUSIONDIRECTORY-JENKINS

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE1}  \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/*


%changelog
* Wed Apr 09 2014 Swaelens Jonathan <swaelens.jonathan@openmailbox.org> - 1-0
- Initial release
