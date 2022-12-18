FROM centos:stream8

RUN yum clean all \
   &&  yum update -y \
   &&  yum clean all

RUN yum install -y gcc gcc-c++ libtool libtool-ltdl make cmake git pkgconfig \
		sudo automake autoconf yum-utils rpm-build \
   &&  yum install -y libxml2 expat-devel openssl-devel libcap \
		libtool-ltdl-devel \
		git autoconf automake libtool gcc-c++ \
		bzip2 ed make openldap-devel pam-devel libxml2-devel \
		libcap-devel vim nettle-devel redhat-lsb-core \
		libtdb-devel libtdb redhat-rpm-config rpm-build rpm-devel \
   &&  yum install -y systemd-units openldap-devel pam-devel openssl-devel \
		krb5-devel expat-devel libxml2-devel libcap-devel libtool \
		libtool-ltdl-devel redhat-rpm-config libdb-devel \
   &&  yum install -y perl-libwww-perl ruby ruby-devel \
   &&  yum clean all

RUN yum update -y \
   &&  yum install -y yum-utils \
   &&  yum install -y systemd-units openldap-devel pam-devel \
		openssl-devel krb5-devel expat-devel \
		libxml2-devel libcap-devel libtool libtool-ltdl-devel \
		redhat-rpm-config libdb-devel \
		gnutls-devel rpmdevtools wget ca-certificates \
   &&  yum clean all


ENV FLAVOR=rpmbuild OS=centos DIST=ol8

CMD ["/srv/pkg"]
