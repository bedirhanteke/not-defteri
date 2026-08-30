Name:           notes
Version:        1.0.0
Release:        1%{?dist}
Summary:        A fast, local Markdown note-taking app for GNOME

License:        GPLv3
URL:            https://example.com/notes
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
Requires:       python3
Requires:       python3-gobject
Requires:       python3-markdown
Requires:       gtk4
Requires:       libadwaita
Requires:       webkit2gtk4.1

%description
A fast, local Markdown note-taking application designed for Fedora and GNOME.

%prep
%autosetup

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}/app
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/scalable/apps

cp -r app/* $RPM_BUILD_ROOT/%{_datadir}/%{name}/app/
cp run.py $RPM_BUILD_ROOT/%{_datadir}/%{name}/

# Create wrapper script
cat << 'EOF' > $RPM_BUILD_ROOT/%{_bindir}/%{name}
#!/bin/bash
exec python3 %{_datadir}/%{name}/run.py "$@"
EOF
chmod +x $RPM_BUILD_ROOT/%{_bindir}/%{name}

cp data/com.example.Notes.desktop $RPM_BUILD_ROOT/%{_datadir}/applications/
cp data/com.example.Notes.svg $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/scalable/apps/

%files
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/com.example.Notes.desktop
%{_datadir}/icons/hicolor/scalable/apps/com.example.Notes.svg

%changelog
* Sun Aug 30 2026 Bedirhan <bedirhan@example.com> - 1.0.0-1
- Initial release
