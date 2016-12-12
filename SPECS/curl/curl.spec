Summary:	An URL retrieval utility and library
Name:		curl
Version:	7.51.0
Release:	2%{?dist}
License:	MIT
URL:		http://curl.haxx.se
Group:		System Environment/NetworkingLibraries
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://curl.haxx.se/download/%{name}-%{version}.tar.lzma
%define sha1 curl=19bf2c1e60a513910355cc9769c6371ea2ff5d1f
Requires:	ca-certificates
BuildRequires:	ca-certificates
Requires:	openssl
BuildRequires:	openssl-devel
Requires:   libssh2
BuildRequires:  libssh2-devel
%description
The cURL package contains an utility and a library used for 
transferring files with URL syntax to any of the following 
protocols: FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, 
DICT, LDAP, LDAPS and FILE. Its ability to both download and 
upload files can be incorporated into other programs to support
functions like streaming media.
%prep
%setup -q
sed -i '/--static-libs)/{N;s#echo .*#echo #;}' curl-config.in
%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--disable-static \
	--enable-threaded-resolver \
	--with-ssl \
	--with-libssh2 \
	--with-ca-bundle=/etc/pki/tls/certs/ca-bundle.crt
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -v -d -m755 %{buildroot}/%{_docdir}/%{name}-%{version}
find %{buildroot}/%{_libdir} -name '*.la' -delete
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so*
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_datarootdir}/aclocal/libcurl.m4
%{_docdir}/%{name}-%{version}
%changelog
*   Wed Nov 30 2016 Xiaolin Li <xiaolinl@vmware.com> 7.51.0-2
-   Enable sftp support.
*   	Wed Nov 02 2016 Anish Swaminathan <anishs@vmware.com> 7.51.0-1
-   	Upgrade curl to 7.51.0
*   	Thu Oct 27 2016 Anish Swaminathan <anishs@vmware.com> 7.47.1-4
-   	Patch for CVE-2016-5421
*   	Mon Sep 19 2016 Xiaolin Li <xiaolinl@vmware.com> 7.47.1-3
-   	Applied CVE-2016-7167.patch.
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.47.1-2
-	GA - Bump release of all rpms
*   	Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 7.47.1-1
-   	Updated to version 7.47.1
* 	Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> 7.46.0-1
- 	Updated to version 7.46.0
*	Thu Aug 13 2015 Divya Thaluru <dthaluru@vmware.com> 7.43.0-1
-	Update to version 7.43.0.
*	Mon Apr 6 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.41.0-1
-	Update to version 7.41.0.
