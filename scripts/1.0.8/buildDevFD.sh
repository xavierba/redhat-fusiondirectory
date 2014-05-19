# Config file for mock
MOCK_CONF="$1"

# FD Branch
BRANCH_FD="$2"

# FD Version
VERSION_FD="$3"

# Jenkins build
JENKINSBUILD="$4"

# Create temporary working directory
TMPDIR="$(mktemp -d)"
cd ${TMPDIR}

# Download src and tar.gz
wget --no-check-certificate https://github.com/fusiondirectory/fusiondirectory/archive/${BRANCH_FD}.zip
unzip ${BRANCH_FD} && rm ${BRANCH_FD}
mv fusiondirectory-${BRANCH_FD}/ fusiondirectory-${VERSION_FD}/
tar -czf fusiondirectory-${VERSION_FD}.tar.gz fusiondirectory-${VERSION_FD}/
rm -Rf fusiondirectory-${VERSION_FD}/

# Create fusiondirectory.spec
cp ${TMPDIR}/* ~/rpmbuild/SOURCES/

# Cat all the spec for the files section
cat /home/jswaelens/dev/template/FD_SPEC \
    /home/jswaelens/dev/template/FD_files \
    /home/jswaelens/dev/scripts/parse/fusiondirectory.files \
    /home/jswaelens/dev/scripts/parse/fusiondirectory-smarty3-acl-render.files \
    /home/jswaelens/dev/template/FD_schema_files \
    /home/jswaelens/dev/scripts/parse/fusiondirectory-schema.files \
    /home/jswaelens/dev/template/FD_plugin_database_connector \
    /home/jswaelens/dev/scripts/parse/fusiondirectory-plugin-database-connector.files \
    > /home/jswaelens/dev/FD.spec


# Replace version and dist in FD spec file
sed -i "s#VERSION_FD#${VERSION_FD}#g" /home/jswaelens/dev/FD.spec
sed -i "s#JENKINSBUILD#jenkinsbuild${JENKINSBUILD}#g" /home/jswaelens/dev/FD.spec

# Create an SRPMS
cd ${TMPDIR}/
mkdir -p ${HOME}/rpmbuild/SOURCES/
mv fusiondirectory-${VERSION_FD}.tar.gz ${HOME}/rpmbuild/SOURCES/
rpmbuild -bs /home/jswaelens/dev/FD.spec

# Compile and test the SRPMS
/usr/bin/mock -r ${MOCK_CONF} clean
/usr/bin/mock -r ${MOCK_CONF} ${HOME}/rpmbuild/SRPMS/fusiondirectory-${VERSION_FD}-jenkinsbuild${JENKINSBUILD}.src.rpm

rm ${HOME}/rpmbuild/SRPMS/fusiondirectory-${VERSION_FD}-jenkinsbuild${JENKINSBUILD}.src.rpm

# Copy the SRPMS and RPMS to build_result
cp -a /var/lib/mock/${MOCK_CONF}/root/builddir/build/SRPMS/* ${HOME}/build_result/SRPMS/
cp -a /var/lib/mock/${MOCK_CONF}/root/builddir/build/RPMS/* ${HOME}/build_result/RPMS/

# Remove TMPDIR
rm -Rf ${TMPDIR}/
