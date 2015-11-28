#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module

%define 	module	httpretty
Summary:	HTTP client mock for Python
Name:		python-%{module}
Version:	0.8.7
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/h/httpretty/httpretty-%{version}.tar.gz
# Source0-md5:	753b82f3bf632fbfc595816a0f6691f0
URL:		https://pypi.python.org/pypi/httpretty
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with python2}
BuildRequires:	python-distribute
BuildRequires:	python-sure
%endif
%if %{with python3}
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
BuildRequires:	python3-sure
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HTTP client mock for Python.

%package -n python3-%{module}
Summary:	HTTP client mock for Python
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
HTTP client mock for Python.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README*
%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README*
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
