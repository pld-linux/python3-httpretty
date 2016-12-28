#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
# Python3 note:
# Due to big API incompatibility between python 3.3, 3.4 and 3.5, the
# author of HTTPretty is **not** supporting python3 officially.  You
# will notice that the travis build for python 3 might be broken, and
# while pull requests fixing py3 support are most welcome, it is still
# not official at least *for now*.
%bcond_without	python3 # CPython 3.x module

%define 	module	httpretty
Summary:	HTTP client mock for Python
Name:		python-%{module}
Version:	0.8.14
Release:	2
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/h/httpretty/httpretty-%{version}.tar.gz
# Source0-md5:	2a6bbf270fafc77647b0479d95d0544c
Patch0:		test-deps.patch
URL:		http://httpretty.readthedocs.io/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-distribute
BuildRequires:	python-sure >= 1.2.24
%if %{with tests}
BuildRequires:	python-httplib2
BuildRequires:	python-nose
BuildRequires:	python-requests
BuildRequires:	python-tornado
%endif
%endif
%if %{with python3}
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
BuildRequires:	python3-sure >= 1.2.24
%if %{with tests}
BuildRequires:	python3-httplib2
BuildRequires:	python3-nose
BuildRequires:	python3-requests
BuildRequires:	python3-tornado
# AUTO: -- ImportError: No module named 'urllib3'
BuildRequires:	python3-urllib3
%endif
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
%patch0 -p1

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
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
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README*
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
