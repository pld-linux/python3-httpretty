#
# Conditional build:
%bcond_with	tests	# unit/functional tests
%bcond_with	doc	# build Sphinx documentation (already built docs included in dist as of 0.9.7)

%define		module	httpretty
Summary:	HTTP client mock for Python
Summary(pl.UTF-8):	Atrapa klienta HTTP dla Pythona
Name:		python3-%{module}
Version:	1.1.4
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/httpretty/
Source0:	https://files.pythonhosted.org/packages/source/h/httpretty/httpretty-%{version}.tar.gz
# Source0-md5:	6f00d23684900c645aba1bb46b2eb320
URL:		https://httpretty.readthedocs.io/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-coverage
BuildRequires:	python3-httplib2
BuildRequires:	python3-rednose
BuildRequires:	python3-requests
BuildRequires:	python3-six >= 1.11.0
BuildRequires:	python3-sure >= 1.2.24
BuildRequires:	python3-tornado
BuildRequires:	python3-urllib3
BuildRequires:	python3-http3
BuildRequires:	python3-botox
BuildRequires:	python3-mock
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HTTP client mock for Python.

%description -l pl.UTF-8
Atrapa klienta HTTP dla Pythona.

%package apidocs
Summary:	API documentation for Python httpretty module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona httpretty
Group:		Documentation

%description apidocs
API documentation for Python httpretty module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona httpretty.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest tests
%endif

%if %{with doc}
sphinx-build-3 -b html -d docs/build/doctrees docs/source docs/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README.rst
%{py3_sitescriptdir}/httpretty
%{py3_sitescriptdir}/httpretty-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_modules,_static,*.html,*.js}
%endif
