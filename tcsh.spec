%define debug_package %nil

Summary:	An enhanced version of csh, the C shell
Name:		tcsh
Version:	6.18.01
Release:	6
License:	BSD
Group:		Shells
URL:		http://www.tcsh.org/
Source0:	ftp://ftp.astron.com/pub/%{name}/%{name}-%{version}.tar.gz

Source1:	alias.csh
# patches from fedora
Patch1:		tcsh-6.15.00-closem.patch
Patch2:		tcsh-aarch64.patch
Patch12:	tcsh-6.15.00-tinfo.patch
Patch13:	tcsh-6.14.00-unprintable.patch
Patch14:	tcsh-6.15.00-hist-sub.patch

# our patches
Patch106:	tcsh-6.10.00-glibc_compat.patch
# handle new DIR_COLORS codes, fixes #40532, #48284 (partly merged)
Patch107:	tcsh-6.17.00-ls-colors-var.patch

BuildRequires:	pkgconfig(ncurses)
BuildRequires:	groff-for-man
Requires(post):	rpm-helper >= 0.7
Requires(postun):	rpm-helper >= 0.7
Provides:	csh = %{version}
Provides:	/bin/csh
Provides:	/bin/tcsh

%description
Tcsh is an enhanced but completely compatible version of csh, the C
shell. Tcsh is a command language interpreter which can be used both
as an interactive login shell and as a shell script command processor.
Tcsh includes a command line editor, programmable word completion,
spelling correction, a history mechanism, job control and a C language
like syntax.


%prep
%setup -q
%patch1 -p0
%patch2 -p1
%patch12 -p0
#patch13 -p1 -b .unprintable
%patch14 -p0

%patch106 -p0
%patch107 -p0

%build
%configure2_5x --bindir=/bin --without-hesiod
%make
nroff -me eight-bit.me > eight-bit.txt

%install
install -D tcsh %{buildroot}/bin/tcsh
install -D tcsh.man %{buildroot}%{_mandir}/man1/tcsh.1

ln -s tcsh.1 %{buildroot}%{_mandir}/man1/csh.1
ln -sf tcsh %{buildroot}/bin/csh

install -D %{SOURCE1} %{buildroot}/etc/profile.d/$(basename %{SOURCE1})

%post
%_add_shell_helper %{name} $1 /bin/csh
%_add_shell_helper %{name} $1 /bin/tcsh

%postun
%_del_shell_helper %{name} $1 /bin/csh
%_del_shell_helper %{name} $1 /bin/tcsh

%files
%defattr(644,root,root,755)
%doc NewThings FAQ Fixes eight-bit.txt complete.tcsh
%doc Ported README* WishList Y2K
%config(noreplace) %{_sysconfdir}/profile.d/*
%attr(755,root,root) /bin/*
%{_mandir}/*/*
