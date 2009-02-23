Summary:	MathML rendering solution for Java
Name:		jeuclid-core
Version:	3.1.4
Release:	%mkrel 1
Group:		Development/Java
License:	ASL 2.0
URL:		http://jeuclid.sourceforge.net/
Source0:	http://downloads.sourceforge.net/jeuclid/jeuclid-parent-%{version}-src.zip
#patch points the ant to the correct jars 
Patch0:		jeuclid-core-build.patch
#removes FreeHep support as per the build README
Patch1:		jeuclid-core-FreeHep.patch
BuildRequires:	jpackage-utils
BuildRequires:	java-rpmbuild
BuildRequires:	ant
BuildRequires:	batik
BuildRequires:	jakarta-commons-logging
BuildRequires:	jcip-annotations
BuildRequires:	xml-commons-apis
BuildRequires:	xmlgraphics-commons >= 1.3.1
Requires:	jpackage-utils
Requires:	java >= 1.5
Requires:	xmlgraphics-commons
Requires:	batik
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Core module containing basic JEuclid rendering and document handling classes.

%prep
%setup -q -n jeuclid-parent-%{version}
%patch0 -p1
%patch1 -p1

#fix line endings
sed 's/\r//' NOTICE > NOTICE.unix
touch -r NOTICE NOTICE.unix;
mv NOTICE.unix NOTICE

find -name '*.jar' -o -name '*.class' -exec rm -f '{}' \;

#removes the FreeHep support from the build per the build README
rm -f jeuclid-core/src/main/java/net/sourceforge/jeuclid/converter/FreeHep*;

%build
cd jeuclid-core
%ant 

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_javadir}
cp -p jeuclid-core/target/jeuclid-core.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar

pushd %{buildroot}%{_javadir}
    for jar in *-%{version}*; do
	ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`
    done
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc NOTICE LICENSE.txt README.Release
%{_javadir}/%{name}*.jar
