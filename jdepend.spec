%define section         free
%define gcj_support     1

Name:           jdepend
Version:        2.9.1
Release:        %mkrel 1.0.3
Epoch:          0
Summary:        Java Design Quality Metrics
License:        BSD-style
Url:            http://www.clarkware.com/
Group:          Development/Java
Source0:        http://www.clarkware.com/software/jdepend-%{version}.zip
BuildRequires:  java-rpmbuild
BuildRequires:  ant
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
JDepend traverses a set of Java class and source file directories and
generates design quality metrics for each Java package. JDepend allows
you to automatically measure the quality of a design in terms of its
extensibility, reusability, and maintainability to effectively manage
and control package dependencies.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%package demo
Summary:        Demos for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
# fix strange permissions
find . -type d -exec chmod 755 {} \;

%build
%{ant} jar javadoc

%install
%{__rm} -rf %{buildroot}

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a build/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
# demo
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr sample $RPM_BUILD_ROOT%{_datadir}/%{name}

# fix end-of-line
%{__perl} -pi -e 's/\r\n/\n/g' README LICENSE

for i in `find docs -type f`; do
    %{__perl} -pi -e 's/\r\n/\n/g' $i
done

for i in `find $RPM_BUILD_ROOT%{_datadir}/%{name} -type f -name "*.java" -o -name "*.properties"`; do
    %{__perl} -pi -e 's/\r\n/\n/g' $i
done

for i in `find $RPM_BUILD_ROOT%{_javadocdir} -type f -name "*.htm*" -o -name "*.css"`; do
    %{__perl} -pi -e 's/\r\n/\n/g' $i
done

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc README LICENSE docs
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%dir %{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}
