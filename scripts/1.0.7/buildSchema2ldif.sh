#!/bin/bash
# Script to use for the build of Schema2ldif in Jenkins
# $1 is the mock_conf
# $2 is the branch of FusionDirectory
# $3 is the version of Schema2ldif

# Variables
HOME="$(pwd ~)"
MOCK_CONF="$1"
SOURCES_FD="http://download.fusiondirectory.org/sources"

BRANCH_FD="$2"
VERSION_SCHEMA2LDIF="$3"

# Usage help
if [ $# -ne 3 ] ; then
  echo "Usage: $(basename $0) <mock_conf> <fd_branch> <schema2ldif_version>"
  exit 1
fi

# Create temporary working directory
TMPDIR="$(mktemp -d)"
cd ${TMPDIR}


# Downoad Checksum and check signature gpg
wget ${SOURCES_FD}/${BRANCH_FD}/schema2ldif/CHECKSUM.MD5

if [ $? -ne 0 ] ; then
  echo "Unable to download the checksum"
  exit 1
fi

# Download signature
wget ${SOURCES_FD}/${BRANCH_FD}/schema2ldif/CHECKSUM.MD5.asc
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
wget ${SOURCES_FD}/${BRANCH_FD}/schema2ldif/schema2ldif-${VERSION_SCHEMA2LDIF}.tar.gz

if [ $? -ne 0 ] ; then
  echo "Unable to download sources archive"
  exit 1
fi

# Download GPG keys for schema2ldif
wget ${SOURCES_FD}/${BRANCH_FD}/schema2ldif/schema2ldif-${VERSION_SCHEMA2LDIF}.tar.gz.asc

if [ $? -ne 0 ] ; then
  echo "Unable to download GPG signature for schema2ldif"
  exit 2
fi

# Verification of GPG signature for schema2ldif
gpg --verify schema2ldif-${VERSION_SCHEMA2LDIF}.tar.gz.asc

if [ $? -ne 0 ] ; then
  echo "Bad Signature for schema2ldif"
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
mv schema2ldif-${VERSION_SCHEMA2LDIF}.tar.gz  ${HOME}/rpmbuild/SOURCES/
rpmbuild -bs ${HOME}/packaging-rpm/redhat/specs/schema2ldif.spec

# Compile and test the SRPMS
/usr/bin/mock -r ${MOCK_CONF} clean
/usr/bin/mock -r ${MOCK_CONF} ${HOME}/rpmbuild/SRPMS/schema2ldif-${VERSION_SCHEMA2LDIF}-1.el6.src.rpm

rm ${HOME}/rpmbuild/SRPMS/schema2ldif-${VERSION_SCHEMA2LDIF}-1.el6.src.rpm

# Copy the SRPMS and RPMS to build_result
cp -a /var/lib/mock/${MOCK_CONF}/root/builddir/build/SRPMS/* ${HOME}/build_result/SRPMS/
cp -a /var/lib/mock/${MOCK_CONF}/root/builddir/build/RPMS/* ${HOME}/build_result/RPMS/

# Remove TMPDIR
rm -Rf ${TMPDIR}/

