#
# note to self: Linus releases need to be named 5.x.0 not 5.x or various
# things break
#
#

%define xm_customver 1

Name:           linux-xmedge-custom
Version:        6.5.5
Release:        100
License:        GPL-2.0
Summary:        The Linux kernel
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://github.com/xanmod/linux/archive/refs/tags/%{version}-xanmod%{xm_customver}.tar.gz
Source1:        config
Source2:        cmdline

%define ktarget  xmedge-custom
%define kversion %{version}-%{release}.%{ktarget}

#BuildRequires:  buildreq-kernel

Requires: systemd-bin
Requires: init-rdahead-extras
Requires: linux-xmedge-custom-license = %{version}-%{release}

# don't strip .ko files!
%global __os_install_post %{nil}
%define debug_package %{nil}
%define __strip /bin/true

#cve.start cve patches from 0001 to 050
#cve.end

#mainline: Mainline patches, upstream backport and fixes from 0051 to 0099
#mainline.end

# Clear patches commented out or not patched in Clear's 6.5 spec file.
# 0113-print-fsync-count-for-bootchart.patch
# 0118-add-scheduler-turbo3-patch.patch
# 0132-prezero-20220308.patch
# 0138-kdf-boottime.patch
# 0200-mm-lru_cache_disable-use-synchronize_rcu_expedited.patch

# Clear patches omitted, due to inclusion in the XanMod kernel.
# 0109-Initialize-ata-before-graphics.patch
# 0112-init-wait-for-partition-and-retry-scan.patch (refer to 0303 below)
# 0115-enable-stateless-firmware-loading.patch
# 0120-do-accept-in-LIFO-order-for-cache-efficiency.patch
# 0121-locking-rwsem-spin-faster.patch
# 0157-scale-net-alloc.patch (refer to 0301 and 0302 below)
# 0001-sched-migrate.patch
# 0002-sched-migrate.patch (XanMod applied the SIS_CURRENT feature)

#Serie.clr 01XX: Clear Linux patches
Patch0101: 0101-i8042-decrease-debug-message-level-to-info.patch
Patch0102: 0102-increase-the-ext4-default-commit-age.patch
Patch0104: 0104-pci-pme-wakeups.patch
Patch0106: 0106-intel_idle-tweak-cpuidle-cstates.patch
Patch0107: 0107-bootstats-add-printk-s-to-measure-boot-time-in-more-.patch
Patch0108: 0108-smpboot-reuse-timer-calibration.patch
Patch0111: 0111-ipv4-tcp-allow-the-memory-tuning-for-tcp-to-go-a-lit.patch
Patch0114: 0114-add-boot-option-to-allow-unsigned-modules.patch
Patch0116: 0116-migrate-some-systemd-defaults-to-the-kernel-defaults.patch
Patch0117: 0117-xattr-allow-setting-user.-attributes-on-symlinks-by-.patch
Patch0122: 0122-ata-libahci-ignore-staggered-spin-up.patch
Patch0123: 0123-print-CPU-that-faults.patch
Patch0125: 0125-nvme-workaround.patch
Patch0126: 0126-don-t-report-an-error-if-PowerClamp-run-on-other-CPU.patch
Patch0127: 0127-lib-raid6-add-patch.patch
Patch0128: 0128-itmt_epb-use-epb-to-scale-itmt.patch
Patch0130: 0130-itmt2-ADL-fixes.patch
Patch0131: 0131-add-a-per-cpu-minimum-high-watermark-an-tune-batch-s.patch
Patch0133: 0133-xm-novector.patch
Patch0134: 0134-md-raid6-algorithms-scale-test-duration-for-speedier.patch
Patch0135: 0135-initcall-only-print-non-zero-initcall-debug-to-speed.patch
Patch0136: scale.patch
Patch0137: libsgrowdown.patch
Patch0139: adlrdt.patch
Patch0141: epp-retune.patch
Patch0142: tcptuning.patch
Patch0143: 0001-powerbump-functionality.patch
Patch0144: 0002-add-networking-support-for-powerbump.patch
Patch0145: 0003-futex-bump.patch
Patch0146: 0001-add-umonitor-umwait-C0.x-C-states.patch
Patch0147: 0001-mm-memcontrol-add-some-branch-hints-based-on-gcov-an.patch
Patch0148: 0002-sched-core-add-some-branch-hints-based-on-gcov-analy.patch
Patch0154: 0136-crypto-kdf-make-the-module-init-call-a-late-init-cal.patch
Patch0155: ratelimit-sched-yield.patch
Patch0158: 0158-clocksource-only-perform-extended-clocksource-checks.patch
Patch0160: better_idle_balance.patch
Patch0161: 0161-ACPI-align-slab-buffers-for-improved-memory-performa.patch
Patch0162: 0162-xm-extra-optmization-flags.patch
Patch0163: 0163-thermal-intel-powerclamp-check-MWAIT-first-use-pr_wa.patch
#Serie.end

#Serie.clr 01XX: Clear Linux conditional patches
Patch0301: scale-net-alloc-6.3.1.patch
Patch0302: scale-net-alloc-6.5.4.patch
Patch0303: 0112-xm-init-wait-for-partition-and-retry-scan.patch
#Serie.end

%description
The Linux kernel.

%package extra
License:        GPL-2.0
Summary:        The Linux kernel extra files
Group:          kernel
Requires:       linux-xmedge-custom-license = %{version}-%{release}

%description extra
Linux kernel extra files

%package license
Summary: license components for the linux package.
Group: Default

%description license
license components for the linux package.

%package cpio
License:        GPL-2.0
Summary:        cpio file with kernel modules
Group:          kernel

%description cpio
Creates a cpio file with some modules

%package dev
License:        GPL-2.0
Summary:        The Linux kernel
Group:          kernel
Requires:       linux-xmedge-custom = %{version}-%{release}
Requires:       linux-xmedge-custom-extra = %{version}-%{release}
Requires:       linux-xmedge-custom-license = %{version}-%{release}

%description dev
Linux kernel build files

%prep
%setup -q -n linux-%{version}-xanmod%{xm_customver}

#cve.patch.start cve patches
#cve.patch.end

#mainline.patch.start Mainline patches, upstream backport and fixes
#mainline.patch.end

#Serie.patch.start Clear Linux patches
%patch -P 101 -p1
%patch -P 102 -p1
%patch -P 104 -p1
%patch -P 106 -p1
%patch -P 107 -p1
%patch -P 108 -p1
%patch -P 111 -p1
%patch -P 114 -p1
%patch -P 116 -p1
%patch -P 117 -p1
%patch -P 122 -p1
%patch -P 123 -p1
%patch -P 125 -p1
%patch -P 126 -p1
%patch -P 127 -p1
%patch -P 128 -p1
%patch -P 130 -p1
%patch -P 131 -p1
%patch -P 133 -p1
%patch -P 134 -p1
%patch -P 135 -p1
%patch -P 136 -p1
%patch -P 137 -p1
%patch -P 139 -p1
%patch -P 141 -p1
%patch -P 142 -p1
%patch -P 143 -p1
%patch -P 144 -p1
%patch -P 145 -p1
%patch -P 146 -p1
%patch -P 147 -p1
%patch -P 148 -p1
%patch -P 154 -p1
%patch -P 155 -p1
%patch -P 158 -p1
%patch -P 160 -p1
%patch -P 161 -p1
%patch -P 162 -p1
%patch -P 163 -p1
#Serie.patch.end

#Serie.patch.start Clear Linux conditional patches
if [ $(grep -c sk_forward_alloc_add include/net/sock.h) == 0 ];
then
%patch -P 301 -p1
else
%patch -P 302 -p1
%patch -P 303 -p1
fi
#Serie.patch.end


cp %{SOURCE1} .config

# Enable preempt.
%if 0
scripts/config -e PREEMPT_BUILD
scripts/config -d PREEMPT_NONE
scripts/config -d PREEMPT_VOLUNTARY
scripts/config -e PREEMPT
scripts/config -e PREEMPT_COUNT
scripts/config -e PREEMPTION
scripts/config -e PREEMPT_DYNAMIC
%endif

# Enable RCU boost (depends on preempt).
%if 0
scripts/config -e RT_MUTEXES
scripts/config -e PREEMPT_RCU
scripts/config -e RCU_EXPERT
scripts/config -e RCU_BOOST
scripts/config --set-val RCU_BOOST_DELAY 500
scripts/config -d RCU_EXP_KTHREAD
%endif

mv .config config

%build
BuildKernel() {

    Target=$1
    Arch=x86_64
    ExtraVer="-%{release}.${Target}"

    rm -f localversion

    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = ${ExtraVer}/" Makefile

    make O=${Target} -s mrproper
    cp config ${Target}/.config

    make O=${Target} -s ARCH=${Arch} olddefconfig
    make O=${Target} -s ARCH=${Arch} CONFIG_DEBUG_SECTION_MISMATCH=y %{?_smp_mflags} %{?sparse_mflags}
}

BuildKernel %{ktarget}

%install

InstallKernel() {

    Target=$1
    Kversion=$2
    Arch=x86_64
    KernelDir=%{buildroot}/usr/lib/kernel
    DevDir=%{buildroot}/usr/lib/modules/${Kversion}/build

    mkdir   -p ${KernelDir}
    install -m 644 ${Target}/.config    ${KernelDir}/config-${Kversion}
    install -m 644 ${Target}/System.map ${KernelDir}/System.map-${Kversion}
    install -m 644 ${Target}/vmlinux    ${KernelDir}/vmlinux-${Kversion}
    install -m 644 %{SOURCE2}           ${KernelDir}/cmdline-${Kversion}
    cp  ${Target}/arch/x86/boot/bzImage ${KernelDir}/org.clearlinux.${Target}.%{version}-%{release}
    chmod 755 ${KernelDir}/org.clearlinux.${Target}.%{version}-%{release}

    mkdir -p %{buildroot}/usr/lib/modules
    make O=${Target} -s ARCH=${Arch} INSTALL_MOD_PATH=%{buildroot}/usr modules_install

    rm -f %{buildroot}/usr/lib/modules/${Kversion}/build
    rm -f %{buildroot}/usr/lib/modules/${Kversion}/source

    mkdir -p ${DevDir}
    find . -type f -a '(' -name 'Makefile*' -o -name 'Kbuild*' -o -name 'Kconfig*' ')' -exec cp -t ${DevDir} --parents -pr {} +
    find . -type f -a '(' -name '*.sh' -o -name '*.pl' ')' -exec cp -t ${DevDir} --parents -pr {} +
    cp -t ${DevDir} -pr ${Target}/{Module.symvers,tools}
    ln -s ../../../kernel/config-${Kversion} ${DevDir}/.config
    ln -s ../../../kernel/System.map-${Kversion} ${DevDir}/System.map
    cp -t ${DevDir} --parents -pr arch/x86/include
    cp -t ${DevDir}/arch/x86/include -pr ${Target}/arch/x86/include/*
    cp -t ${DevDir}/include -pr include/*
    cp -t ${DevDir}/include -pr ${Target}/include/*
    cp -t ${DevDir} --parents -pr scripts/*
    cp -t ${DevDir}/scripts -pr ${Target}/scripts/*
    find  ${DevDir}/scripts -type f -name '*.[cho]' -exec rm -v {} +
    find  ${DevDir} -type f -name '*.cmd' -exec rm -v {} +
    # Cleanup any dangling links
    find ${DevDir} -type l -follow -exec rm -v {} +

    # Kernel default target link
    ln -s org.clearlinux.${Target}.%{version}-%{release} %{buildroot}/usr/lib/kernel/default-${Target}
}

# cpio file for keyboard drivers
createCPIO() {

    Target=$1
    Kversion=$2
    KernelDir=%{buildroot}/usr/lib/kernel
    ModDir=/usr/lib/modules/${Kversion}

    mkdir -p cpiofile${ModDir}/kernel/drivers/input/{serio,keyboard}
    mkdir -p cpiofile${ModDir}/kernel/drivers/hid
    cp %{buildroot}${ModDir}/kernel/drivers/input/serio/i8042.ko      cpiofile${ModDir}/kernel/drivers/input/serio
    cp %{buildroot}${ModDir}/kernel/drivers/input/serio/libps2.ko     cpiofile${ModDir}/kernel/drivers/input/serio
    cp %{buildroot}${ModDir}/kernel/drivers/input/keyboard/atkbd.ko   cpiofile${ModDir}/kernel/drivers/input/keyboard
    cp %{buildroot}${ModDir}/kernel/drivers/hid/hid-logitech-dj.ko    cpiofile${ModDir}/kernel/drivers/hid
    cp %{buildroot}${ModDir}/kernel/drivers/hid/hid-logitech-hidpp.ko cpiofile${ModDir}/kernel/drivers/hid
    cp %{buildroot}${ModDir}/kernel/drivers/hid/hid-apple.ko          cpiofile${ModDir}/kernel/drivers/hid
    cp %{buildroot}${ModDir}/modules.order   cpiofile${ModDir}
    cp %{buildroot}${ModDir}/modules.builtin cpiofile${ModDir}

    depmod -b cpiofile/usr ${Kversion}

    (
      cd cpiofile
      find . | cpio --create --format=newc \
        | xz --check=crc32 --lzma2=dict=1024KiB > ${KernelDir}/initrd-org.clearlinux.${Target}.%{version}-%{release}
    )
}

InstallKernel %{ktarget} %{kversion}

createCPIO %{ktarget} %{kversion}

rm -rf %{buildroot}/usr/lib/firmware

mkdir -p %{buildroot}/usr/share/package-licenses/linux-xmedge-custom
cp COPYING %{buildroot}/usr/share/package-licenses/linux-xmedge-custom/COPYING
cp -a LICENSES/* %{buildroot}/usr/share/package-licenses/linux-xmedge-custom

%postun
rm -fr /var/lib/dkms/*/kernel-%{kversion}-x86_64
rm -fr /var/lib/dkms/*/*/%{kversion}

%files
%dir /usr/lib/kernel
%dir /usr/lib/modules/%{kversion}
/usr/lib/kernel/config-%{kversion}
/usr/lib/kernel/cmdline-%{kversion}
/usr/lib/kernel/org.clearlinux.%{ktarget}.%{version}-%{release}
/usr/lib/kernel/default-%{ktarget}
/usr/lib/modules/%{kversion}/kernel
/usr/lib/modules/%{kversion}/modules.*

%files extra
%dir /usr/lib/kernel
/usr/lib/kernel/System.map-%{kversion}
/usr/lib/kernel/vmlinux-%{kversion}

%files license
%defattr(0644,root,root,0755)
/usr/share/package-licenses/linux-xmedge-custom

%files cpio
/usr/lib/kernel/initrd-org.clearlinux.%{ktarget}.%{version}-%{release}

%files dev
%defattr(-,root,root)
/usr/lib/modules/%{kversion}/build
