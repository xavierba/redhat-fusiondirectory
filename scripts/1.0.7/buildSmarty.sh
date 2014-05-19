#!/bin/bash
# Script to use for the build of Smarty in Jenkins
# $1 is the mock_conf
# $2 is the branch of FusionDirectory
# $3 is the version of Smarty3
# $4 is the version of smarty3-i18n

# Variables
HOME="$(pwd ~)"
MOCK_CONF="$1"

SOURCES_FD="http://download.fusiondirectory.org/sources"
SOURCES_SMARTY3="http://www.smarty.net/files"

BRANCH_FD="$2"
VERSION_SMARTY3="$3"
VERSION_smarty3_i18n="$4"


# Usage help
if [ $# -ne 4 ] ; then
  echo "Usage: $(basename $0) <mock_conf> <fd_branch> <Smarty3_version> <smarty3-i18n_version>"
  exit 1
fi


# Create temporary working directory
TMPDIR="$(mktemp -d)"
cd ${TMPDIR}


# Downoad Checksum and check signature gpg
wget ${SOURCES_FD}/${BRANCH_FD}/smarty3-i18n/CHECKSUM.MD5

if [ $? -ne 0 ] ; then
  echo "Unable to download the checksum"
  exit 1
fi

# Download signature
wget ${SOURCES_FD}/${BRANCH_FD}/smarty3-i18n/CHECKSUM.MD5.asc
if [ $? -ne 0 ] ; then
  echo "Unable to download GPG signature for the checksum"
  exit 2
fi

# Verifying signature for the checksum
gpg --verify CHECKSUM.MD5.asc

if [ $? -ne 0 ] ; then
  echo "Bad Signature for core component"
  exit 3
fi


# Download sources for Smarty3 and smarty3-i18n
wget ${SOURCES_SMARTY3}/Smarty-${VERSION_SMARTY3}.tar.gz
wget ${SOURCES_FD}/${BRANCH_FD}/smarty3-i18n/smarty3-i18n-${VERSION_smarty3_i18n}.tar.gz

if [ $? -ne 0 ] ; then
  echo "Unable to download sources archive"
  exit 1
fi

# Download GPG keys for smarty3-i18n
wget ${SOURCES_FD}/${BRANCH_FD}/smarty3-i18n/smarty3-i18n-${VERSION_smarty3_i18n}.tar.gz.asc
#
if [ $? -ne 0 ] ; then
  echo "Unable to download GPG signature for smarty3-i18n"
  exit 2
fi

# Verification of GPG signature for smarty3-i18n
gpg --verify smarty3-i18n-${VERSION_smarty3_i18n}.tar.gz.asc

if [ $? -ne 0 ] ; then
  echo "Bad Signature for smarty3-i18n"
  exit 3
fi


# Verify the MD5 for the tar.gz
cat CHECKSUM.MD5 | grep "${VERSION_smarty3_i18n}" | md5sum -c -
if [ $? -ne 0 ] ; then
  echo "Error in the verification of the MD5 in the tar.gz"
  exit 4
fi


# Create an SRPMS
mkdir -p ${HOME}/rpmbuild/SOURCES/
mv Smarty-${VERSION_SMARTY3}.tar.gz smarty3-i18n-${VERSION_smarty3_i18n}.tar.gz  ${HOME}/rpmbuild/SOURCES/
rpmbuild -bs ${HOME}/packaging-rpm/redhat/specs/php-Smarty3.spec

# Compile and test the SRPMS
/usr/bin/mock -r ${MOCK_CONF} clean
/usr/bin/mock -r ${MOCK_CONF} ${HOME}/rpmbuild/SRPMS/php-Smarty3-${VERSION_SMARTY3}-1.el6.src.rpm

# Copy the SRPMS and RPMS to build_result
cp -a /var/lib/mock/${MOCK_CONF}/root/builddir/build/SRPMS/* ${HOME}/build_result/SRPMS/
cp -a /var/lib/mock/${MOCK_CONF}/root/builddir/build/RPMS/* ${HOME}/build_result/RPMS/

rm ${HOME}/rpmbuild/SRPMS/php-Smarty3-${VERSION_SMARTY3}-1.el6.src.rpm
rm ${HOME}/rpmbuild/SRPMS/php-Smarty3-i18n-${VERSION_smarty3_i18n}-1.el6.src.rpm

rpmbuild -bs ${HOME}/packaging-rpm/redhat/specs/php-Smarty3-i18n.spec
/usr/bin/mock -r ${MOCK_CONF} clean
/usr/bin/mock -r ${MOCK_CONF} ${HOME}/rpmbuild/SRPMS/php-Smarty3-i18n-${VERSION_smarty3_i18n}-1.el6.src.rpm

# Copy the SRPMS and RPMS to build_result
cp -a /var/lib/mock/${MOCK_CONF}/root/builddir/build/SRPMS/* ${HOME}/build_result/SRPMS/
cp -a /var/lib/mock/${MOCK_CONF}/root/builddir/build/RPMS/* ${HOME}/build_result/RPMS/
# Remove TMPDIR
rm -Rf ${TMPDIR}/

