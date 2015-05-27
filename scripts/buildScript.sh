#!/bin/bash
# Script that build RPM packages

##############################

# Variables
# Mock conf
MOCK_CONF='epel-6-i386'

# RPMBUILD directory
RPMBUILD="$HOME/rpmbuild"

# BUILD directory
BUILDDIR="$HOME/build_result"

# Version
version=''

# Sub version
jenkinssubversion=''

# Package
package=''

# Download by source (default false)
DOWNLOAD_BY_SPEC='0'

##############################

usage() {
  cat << EOF
Usage: $0 -p package -c subversion -s SPECDIR [-v version] [-m MOCK_CONF] [-r RPMBUILD] [-b BUILDDIR] [-d]
  Default values:
    MOCK_CONF='epel-6-i386'
    RPMBUILD='~/rpmbuild'
    BUILDDIR='~/build_result'
    version='Version in specfile'
  You can use -d for download the source by spec.
EOF
}

function removeDependancies()
{
  # Remove old dependances
  sudo yum remove perl-DateTime-TimeZone perl-Net-LDAP-Server -y
}

function createDirectories()
{
  mkdir -p $BUILDDIR/RPMS/
  mkdir -p $BUILDDIR/SRPMS/
  
  mkdir -p $RPMBUILD/SOURCES/
  mkdir -p $RPMBUILD/SPECS/
  mkdir -p $RPMBUILD/RPMS/
  mkdir -p $RPMBUILD/SRPMS/
}

# Create new SPEC
function createSpec()
{
  # Create new spec with good version and sub version
  cp $SPECDIR/$package.spec $RPMBUILD/SPECS/$package.spec
  
  if [ $version ] ; then
    sed -i "s/_VERSION_/$version/g" "$RPMBUILD/SPECS/$package.spec"
  else
    VERSION="$(echo $(cat  $RPMBUILD/SPECS/$package.spec | grep 'Version:' | cut -d ':' -f2))"
    sed -i "s/_VERSION_/$VERSION/g" "$RPMBUILD/SPECS/$package.spec"
  fi 
  
  sed -i "s/_RELEASE_/$jenkinssubversion/g" "$RPMBUILD/SPECS/$package.spec"

  if [ "$package" = 'POE-Component-Server-JSONRPC' ] ; then
    # Add -bis in SRC
    sed -i 's/\(^Source.*\)\(%{version}\)\(.*$\)/\1%{version}-bis\3/' "$RPMBUILD/SPECS/$package.spec"
  fi
}

# Download src
function downloadSrcBySpec()
{
  # Grab version
  VERSION="$(echo $(cat  $RPMBUILD/SPECS/$package.spec | grep 'Version:' | cut -d ':' -f2))"

  # Grab source URL
  SRC="$(echo $(cat  $RPMBUILD/SPECS/$package.spec | grep 'Source0' | cut -d ':' -f3 | sed "s/%{version}/$VERSION/g"))"

  # Download SRC
  cd $RPMBUILD/SOURCES/
  wget "http:$SRC" || exit 2

  # Copy the copyrights
  # cp /home/jswaelens/redhat/sources/argonaut-libs/* $RPMBUILD/SOURCES/
}

# Build RPM
function build()
{
  # Build RPM and SRPMS and test with mock if possible
  # Clean mock directory
  /usr/bin/mock -r ${MOCK_CONF} clean

  # Grab version
  VERSION="$(echo $(cat  $RPMBUILD/SPECS/$package.spec | grep 'Version:' | cut -d ':' -f2))"

  # Create SRPMS
  rpmbuild -bs $RPMBUILD/SPECS/$package.spec || exit 2

  if [ "$package" = 'perl-POE-Component-Schedule' ] ; then
    sudo yum install perl-DateTime-Set $BUILDDIR/RPMS/perl-DateTime-TimeZone* -y
    rpmbuild -ba $RPMBUILD/SPECS/$package.spec || exit 2

   # Move the packages rpmbuild
   mv $RPMBUILD/SRPMS/* $BUILDDIR/SRPMS/
   mv $RPMBUILD/RPMS/noarch/* $BUILDDIR/RPMS/

  elif [ "$package" = 'perl-POE-Component-Server-SimpleHTTP' ] ; then
    rpmbuild -ba $RPMBUILD/SPECS/$package.spec || exit 2

   # Move the packages rpmbuild
   mv $RPMBUILD/SRPMS/* $BUILDDIR/SRPMS/
   mv $RPMBUILD/RPMS/noarch/* $BUILDDIR/RPMS/


  elif [ "$package" = 'perl-MooseX-POE' ] ; then
    rpmbuild -ba $RPMBUILD/SPECS/$package.spec || exit 2

   # Move the packages rpmbuild
   mv $RPMBUILD/SRPMS/* $BUILDDIR/SRPMS/
   mv $RPMBUILD/RPMS/noarch/* $BUILDDIR/RPMS/

  else
    NAME="$(echo $(cat  $RPMBUILD/SPECS/$package.spec | grep 'Name:' | cut -d ':' -f2))"
    /usr/bin/mock -r ${MOCK_CONF} $RPMBUILD/SRPMS/${NAME}-${VERSION}-${jenkinssubversion}.src.rpm || exit 2

    # Move the packages of mock
    mv /var/lib/mock/${MOCK_CONF}/root/builddir/build/SRPMS/* $BUILDDIR/SRPMS/
    mv /var/lib/mock/${MOCK_CONF}/root/builddir/build/RPMS/* $BUILDDIR/RPMS/
  fi
}

##############################

while getopts "p:v:c:m:r:b:s:h -- d" opt; do
  case "$opt" in
    p)
      package=$OPTARG
      ;;
    v)
      version=$OPTARG
      ;;
    c)
      jenkinssubversion=$OPTARG
      ;;
    m)
      MOCK_CONF=$OPTARG
      ;;
    r)
      RPMBUILD=$OPTARG
      ;;
    b)
      BUILDDIR=$OPTARG
      ;;
    s)
      SPECDIR=$OPTARG
      ;;
    d)
      DOWNLOAD_BY_SPEC='1'
      ;;
    h)
      usage
      exit 0
      ;;
    *)
      usage
      exit 1
      ;;
  esac
done

##############################

if [ ! $package ] ; then
  usage
  exit 1
fi

if [ ! $jenkinssubversion ] ; then
  usage
  exit 1
fi

if [ ! $SPECDIR ] ; then
  usage
  exit 1
fi

shift $((OPTIND-1))

removeDependancies

createDirectories

createSpec

if [ "$DOWNLOAD_BY_SPEC" = '1' ] ; then
  downloadSrcBySpec
fi

build

