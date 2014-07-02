# Not use mock for this file he must have an personnal version of perl-DateTime-TimeZone!!!

Name:           perl-POE-Component-Schedule
Version:        _VERSION_
Release:        1%{dist}
Summary:        Schedule POE events using DateTime::Set iterators
License:	Artistic or GPL-1+
Group:          Development/Libraries

URL:            http://search.cpan.org/dist/POE-Component-Schedule/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DO/DOLMEN/POE-Component-Schedule-%{version}.tar.gz
Source1:	copyright-POE-Component-Schedule
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch
BuildRequires:  perl, perl-ExtUtils-MakeMaker, perl-DateTime, perl-DateTime-Set
BuildRequires:	perl-POE, perl-Module-Build
BuildRequires:	perl(Test::More)
BuildRequires:	perl-DateTime-TimeZone >= 1.13

Requires:	perl, perl-POE >= 1.287, perl-DateTime >= 0.48
Requires:	perl-DateTime-Set >= 0.25, perl-DateTime-TimeZone >= 1.13

%description
This perl module is a POE component that sends events to POE client sessions on
a schedule defined by a DateTime::Set iterator.

%prep
%setup -T -D -b 0 -n POE-Component-Schedule-%{version}
cp ${HOME}/rpmbuild/SOURCES/copyright-POE-Component-Schedule ./copyright


%build
perl Build.PL
./Build

%check
# Test not work on this vm!
#./Build test

%install
# Grab perl version for the directory
PERLDIR='perl5'

# Go into the directory
cd ./blib/

# Remove all the .exists
find . -name '.exists' -exec rm "{}" \;

# Create directories in buildroot
mkdir -p %{buildroot}/usr/share/man/man3/
mkdir -p %{buildroot}/usr/share/${PERLDIR}/

# Copy files in buildroot
cp ./libdoc/* %{buildroot}/usr/share/man/man3/
cp -a ./lib/POE/ %{buildroot}/usr/share/${PERLDIR}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_mandir}/man3/*
/usr/share/perl5/POE/Component/*

%doc Changes README copyright

%changelog
* Fri May 9 2014 Jonathan SWAELENS <swaelens.jonathan@openmailbox.org>
- Initial Release
