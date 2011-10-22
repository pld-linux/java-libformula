#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%define		srcname		libformula
%include	/usr/lib/rpm/macros.java
Summary:	Formula Parser
Name:		java-%{srcname}
Version:	1.1.3
Release:	1
License:	LGPL v2+
Group:		Libraries/Java
Source0:	http://downloads.sourceforge.net/jfreereport/%{srcname}-%{version}.zip
# Source0-md5:	5ec40c55999fe45d07553b42388ef585
Patch0:		build.patch
URL:		http://reporting.pentaho.org/
BuildRequires:	ant
BuildRequires:	ant-contrib
BuildRequires:	ant-nodeps
BuildRequires:	java-libbase >= 1.1.3
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jakarta-commons-logging
Requires:	java-libbase >= 1.1.3
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibFormula provides Excel-Style-Expressions. The implementation
provided here is very generic and can be used in any application that
needs to compute formulas.

%package javadoc
Summary:	Javadoc for LibFormula
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for LibFormula.

%prep
%setup -qc
%patch0 -p1
find -name "*.jar" | xargs rm -v
install -d lib
ln -s %{_javadir}/ant lib/ant-contrib

%build
build-jar-repository -s -p lib commons-logging-api libbase
%ant jar %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a dist/%{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a bin/javadoc/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc licence-LGPL.txt README.txt ChangeLog.txt
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
