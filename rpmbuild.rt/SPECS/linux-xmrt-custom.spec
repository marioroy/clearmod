#
# This is the kernel native kernel plus the Preempt-RT patches
#
#
#

%define xm_customver 1
%define xm_customver_rt 15

Name:           linux-xmrt-custom
Version:        6.1.54
Release:        102
License:        GPL-2.0
Summary:        The Linux kernel with Preempt-RT patch
Url:            https://www.kernel.org
Group:          kernel
Source0:        https://github.com/xanmod/linux/archive/refs/tags/%{version}-rt%{xm_customver_rt}-xanmod%{xm_customver}.tar.gz
Source1:        config
Source2:        cmdline

%define ktarget  xmrt-custom
%define kversion %{version}-%{release}.%{ktarget}

#BuildRequires:  buildreq-kernel

Requires: systemd-bin
Requires: init-rdahead-extras
Requires: linux-xmrt-custom-license = %{version}-%{release}

# don't strip .ko files!
%global __os_install_post %{nil}
%define debug_package %{nil}
%define __strip /bin/true

#cve.start cve patches from 0001 to 050
#cve.end

#mainline: Mainline patches, upstream backport and fixes from 0051 to 0099
#mainline.end

# Clear patches commented out or not patched in Clear's 6.1 RT spec file.
# 0110-give-rdrand-some-credit.patch
# 0112-kernel-time-reduce-ntp-wakeups.patch
# 0114-print-fsync-count-for-bootchart.patch
# 0127-x86-microcode-echo-2-reload-to-force-load-ucode.patch
# Clear patch not applied, sched_set_itmt_core_prio is same as LTS kernel.
# 0119-add-scheduler-turbo3-patch.patch

# Clear patches not applied, due to inclusion in the XanMod kernel.
# 0103-silence-rapl.patch
# 0109-Initialize-ata-before-graphics.patch
# 0113-init-wait-for-partition-and-retry-scan.patch
# 0116-Enable-stateless-firmware-loading.patch
# 0121-do-accept-in-LIFO-order-for-cache-efficiency.patch
# 0123-locking-rwsem-spin-faster.patch

#Serie.clr 01XX: Clear Linux patches
Patch0101: 0101-i8042-decrease-debug-message-level-to-info.patch
Patch0102: 0102-Increase-the-ext4-default-commit-age.patch
Patch0104: 0104-pci-pme-wakeups.patch
Patch0105: 0105-ksm-wakeups.patch
Patch0106: 0106-intel_idle-tweak-cpuidle-cstates.patch
Patch0107: 0107-bootstats-add-printk-s-to-measure-boot-time-in-more-.patch
Patch0108: 0108-smpboot-reuse-timer-calibration.patch
Patch0111: 0111-ipv4-tcp-allow-the-memory-tuning-for-tcp-to-go-a-lit.patch
Patch0115: 0115-Add-boot-option-to-allow-unsigned-modules.patch
Patch0117: 0117-Migrate-some-systemd-defaults-to-the-kernel-defaults.patch
Patch0118: 0118-xattr-allow-setting-user.-attributes-on-symlinks-by-.patch
Patch0122: 0122-zero-extra-registers.patch
Patch0124: 0124-ata-libahci-ignore-staggered-spin-up.patch
Patch0125: 0125-print-CPU-that-faults.patch
Patch0126: 0126-x86-microcode-Force-update-a-uCode-even-if-the-rev-i.patch
Patch0128: 0128-fix-bug-in-ucode-force-reload-revision-check.patch
Patch0129: 0129-nvme-workaround.patch
Patch0130: 0130-Don-t-report-an-error-if-PowerClamp-run-on-other-CPU.patch
Patch0131: 0131-overload-on-wakeup.patch
Patch0133: 0133-xm-novector.patch
#Serie.end

%description
The Linux kernel.

%package extra
License:        GPL-2.0
Summary:        The Linux kernel extra files
Group:          kernel
Requires:       linux-xmrt-custom-license = %{version}-%{release}

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
Requires:       linux-xmrt-custom = %{version}-%{release}
Requires:       linux-xmrt-custom-extra = %{version}-%{release}
Requires:       linux-xmrt-custom-license = %{version}-%{release}

%description dev
Linux kernel build files

%prep
%setup -q -n linux-%{version}-rt%{xm_customver_rt}-xanmod%{xm_customver}

#cve.patch.start cve patches
#cve.patch.end

#mainline.patch.start Mainline patches, upstream backport and fixes
#mainline.patch.end

#Serie.patch.start Clear Linux patches
%patch -P 101 -p1
%patch -P 102 -p1
%patch -P 104 -p1
%patch -P 105 -p1
%patch -P 106 -p1
%patch -P 107 -p1
%patch -P 108 -p1
%patch -P 111 -p1
%patch -P 115 -p1
%patch -P 117 -p1
%patch -P 118 -p1
%patch -P 122 -p1
%patch -P 124 -p1
%patch -P 125 -p1
%patch -P 126 -p1
%patch -P 128 -p1
%patch -P 129 -p1
%patch -P 130 -p1
%patch -P 131 -p1
%patch -P 133 -p1
#Serie.patch.end


cp %{SOURCE1} .config

# Run equally well on all x86-64 CPUs with min support of x86-64-v3.
scripts/config -d MCORE2
scripts/config -e GENERIC_CPU3

# Change tick rate to 500 HZ, XanMod default.
scripts/config -d HZ_1000
scripts/config -e HZ_500
scripts/config --set-val HZ 500

# Disable tracers, XanMod default.
scripts/config -d DMA_FENCE_TRACE
scripts/config -d DRM_I915_LOW_LEVEL_TRACEPOINTS
scripts/config -d RCU_TRACE
scripts/config -d FTRACE

# Enable WINESYNC driver for fast kernel-backed Wine.
scripts/config -e WINESYNC

# If preempt is desired, choose preempt or preempt_rt.
# preempt_rt overrides preempt knobs if both enabled

# Enable preempt.
%if 0
scripts/config -e PREEMPT_BUILD
scripts/config -d PREEMPT_NONE
scripts/config -d PREEMPT_VOLUNTARY
scripts/config -e PREEMPT
scripts/config -e PREEMPT_DYNAMIC
scripts/config -e PREEMPT_COUNT
scripts/config -e PREEMPTION
%endif

# Enable preempt_rt.
%if 0
scripts/config -e PREEMPT_BUILD
scripts/config -d PREEMPT_NONE
scripts/config -d PREEMPT_VOLUNTARY
scripts/config -d PREEMPT
scripts/config -d PREEMPT_DYNAMIC
scripts/config -e PREEMPT_RT
scripts/config -e PREEMPT_COUNT
scripts/config -e PREEMPTION
%endif

# Enable RCU boost (depends on preempt or preempt_rt).
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

    rm -f localversion-rt localversion-xanmod

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
        | xz --check=crc32 --lzma2=dict=512KiB > ${KernelDir}/initrd-org.clearlinux.${Target}.%{version}-%{release}
    )
}

InstallKernel %{ktarget} %{kversion}

createCPIO %{ktarget} %{kversion}

rm -rf %{buildroot}/usr/lib/firmware

mkdir -p %{buildroot}/usr/share/package-licenses/linux-xmrt-custom
cp COPYING %{buildroot}/usr/share/package-licenses/linux-xmrt-custom/COPYING
cp -a LICENSES/* %{buildroot}/usr/share/package-licenses/linux-xmrt-custom

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
/usr/share/package-licenses/linux-xmrt-custom

%files cpio
/usr/lib/kernel/initrd-org.clearlinux.%{ktarget}.%{version}-%{release}

%files dev
%defattr(-,root,root)
/usr/lib/modules/%{kversion}/build
