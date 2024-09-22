#
# Linux releases need to be named 6.x.0 not 6.x or various things break.
#
%define   xm_customver 1

Name:     linux-xmbore
Version:  6.10.11
Release:  198
License:  GPL-2.0
Summary:  The Linux kernel
Url:      http://www.kernel.org/
Group:    kernel
Source0:  https://github.com/xanmod/linux/archive/refs/tags/%{version}-xanmod%{xm_customver}.tar.gz
Source1:  config
Source2:  cmdline

Requires: linux-xmbore-license = %{version}-%{release}

# Build requires: swupd bundle-add \
#   bc bison c-basic devpkg-gmp devpkg-elfutils devpkg-openssl flex \
#   kernel-install linux-firmware lz4 make package-utils wget xz

%define ktarget  xmbore
%define kversion %{version}-%{release}.%{ktarget}

# don't strip .ko files!
%global __os_install_post %{nil}
%define debug_package %{nil}
%define __strip /bin/true

#mainline: Mainline patches, upstream backport and fixes from 0051 to 0099
#mainline.end

# Clear patches omitted, due to inclusion in the XanMod kernel.
# 0109-initialize-ata-before-graphics.patch
# 0115-enable-stateless-firmware-loading.patch
# 0120-do-accept-in-LIFO-order-for-cache-efficiency.patch
# 0121-locking-rwsem-spin-faster.patch

# Clear patch omitted, due to higher latency regression.
# 0167-net-sock-increase-default-number-of-_SK_MEM_PACKETS-.patch

#Serie.clr 01XX: Clear Linux patches
Patch0101: 0101-i8042-decrease-debug-message-level-to-info.patch
Patch0102: 0102-increase-the-ext4-default-commit-age.patch
Patch0104: 0104-pci-pme-wakeups.patch
Patch0106: 0106-intel_idle-tweak-cpuidle-cstates.patch
Patch0108: 0108-smpboot-reuse-timer-calibration.patch
Patch0111: 0111-ipv4-tcp-allow-the-memory-tuning-for-tcp-to-go-a-lit.patch
Patch0112: 0112-init-wait-for-partition-and-retry-scan.patch
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
Patch0137: libsgrowdown.patch
Patch0141: epp-retune.patch
Patch0148: 0002-sched-core-add-some-branch-hints-based-on-gcov-analy.patch
Patch0154: 0136-crypto-kdf-make-the-module-init-call-a-late-init-cal.patch
Patch0155: ratelimit-sched-yield.patch
Patch0157: scale-net-alloc.patch
Patch0158: 0158-clocksource-only-perform-extended-clocksource-checks.patch
Patch0160: better_idle_balance.patch
Patch0161: 0161-ACPI-align-slab-buffers-for-improved-memory-performa.patch
Patch0163: 0163-thermal-intel-powerclamp-check-MWAIT-first-use-pr_wa.patch
Patch0164: 0164-KVM-VMX-make-vmx-init-a-late-init-call-to-get-to-ini.patch
Patch0165: slack.patch
Patch0166: 0166-sched-fair-remove-upper-limit-on-cpu-number.patch
#Serie.end

# Burst-Oriented Response Enhancer (BORE) CPU Scheduler.
# The CONFIG_SCHED_BORE knob is enabled by default.
# https://github.com/firelzrd/bore-scheduler
Patch2000: 0001-linux6.10.y-bore.patch

# Revert yield_type sysctl to reduce or disable sched_yield.
Patch2100: xanmod-revert-yield_type-sysctl.patch

# Add HZ_625 and HZ_800 timer-tick options.
# https://gist.github.com/marioroy/f383f1e9f18498a251beb5c0a9f33dcf
Patch2101: xanmod-hz-625-800-timer-frequencies.patch

# Add "ASUS PRIME TRX40 PRO-S" entry to usbmix_ctl_maps.
# To resolve "cannot get min/max values for control 12 (id 19)".
# https://bugzilla.kernel.org/show_bug.cgi?id=206543
Patch2102: asus-prime-trx40-pro-s-mixer-def.patch

# Scheduler updates.
Patch2103: sched_fair_make_SCHED_IDLE_be_preempted.patch

# v4l2-loopback device.
Patch2201: v4l2loopback.patch

# CachyOS 6.10 fixes and NTSYNC update.
Patch2202: 0006-linux6.10-fixes.patch
Patch2203: 0009-linux6.10-ntsync.patch

%description
The Linux kernel.

%package extra
License:        GPL-2.0
Summary:        The Linux kernel extra files
Group:          kernel
Requires:       linux-xmbore-license = %{version}-%{release}

%description extra
Linux kernel extra files

%package license
Summary:        license components for the linux package.
Group:          Default

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
Requires:       linux-xmbore = %{version}-%{release}
Requires:       linux-xmbore-extra = %{version}-%{release}
Requires:       linux-xmbore-license = %{version}-%{release}

%description dev
Linux kernel build files

%prep
%setup -q -n linux-%{version}-xanmod%{xm_customver}

#mainline.patch.start Mainline patches, upstream backport and fixes
#mainline.patch.end

#Serie.patch.start Clear Linux patches
%patch -P 101 -p1
%patch -P 102 -p1
%patch -P 104 -p1
%patch -P 106 -p1
%patch -P 108 -p1
%patch -P 111 -p1
%patch -P 112 -p1
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
%patch -P 137 -p1
%patch -P 141 -p1
%patch -P 148 -p1
%patch -P 154 -p1
%patch -P 155 -p1
%patch -P 157 -p1
%patch -P 158 -p1
%patch -P 160 -p1
%patch -P 161 -p1
%patch -P 163 -p1
%patch -P 164 -p1
%patch -P 165 -p1
%patch -P 166 -p1
#Serie.patch.end

cat %{PATCH2000} | \
  sed 's/scaling = SCHED_TUNABLESCALING_LOG/scaling = SCHED_TUNABLESCALING_NONE/' | \
  patch --no-backup-if-mismatch -p1

%patch -P 2100 -p1
%patch -P 2101 -p1
%patch -P 2102 -p1
%patch -P 2103 -p1
%patch -P 2201 -p1
%patch -P 2202 -p1
%patch -P 2203 -p1


cp %{SOURCE1} .config

# Run equally well on all x86-64 CPUs with minimum support of x86-64-v3.
scripts/config -d MCORE2
scripts/config -e GENERIC_CPU3

# Set timer frequency { 100, 250, 300, 500, 625, 800, or 1000 }.
# Defaults to 800Hz tick rate.
scripts/config -d HZ_1000
scripts/config -e HZ_%{_hzval}

# Default to maximum amount of ASLR bits.
scripts/config --set-val ARCH_MMAP_RND_BITS 32
scripts/config --set-val ARCH_MMAP_RND_COMPAT_BITS 16

# Disable using efivars as a pstore backend by default.
scripts/config -m EFI_VARS_PSTORE
scripts/config -e EFI_VARS_PSTORE_DEFAULT_DISABLE

# The frame pointer unwinder degrades overall performance by roughly 5-10%.
# Default to the ORC (Oops Rewind Capability) unwinder. (XanMod default)
scripts/config -d UNWINDER_FRAME_POINTER
scripts/config -e UNWINDER_ORC

# Disable kernel tracing infrastructure and call depth tracking. (XanMod default)
scripts/config -d FTRACE
scripts/config -d MITIGATION_CALL_DEPTH_TRACKING

# Disable debug.
%if 1
scripts/config -d GDB_SCRIPTS
scripts/config -d DEBUG_BUGVERBOSE
scripts/config -d DEBUG_INFO
scripts/config -d DEBUG_INFO_BTF
scripts/config -d DEBUG_INFO_BTF_MODULES
scripts/config -d DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT
scripts/config -d DEBUG_INFO_DWARF4
scripts/config -d DEBUG_INFO_DWARF5
scripts/config -e DEBUG_INFO_NONE
scripts/config -d DEBUG_LIST
scripts/config -d DEBUG_PREEMPT
scripts/config -d PAHOLE_HAS_SPLIT_BTF
scripts/config -d SLUB_DEBUG
scripts/config -d ACPI_DEBUG
scripts/config -d PM_DEBUG
scripts/config -d PM_ADVANCED_DEBUG
scripts/config -d PM_SLEEP_DEBUG
scripts/config -d IRQ_TIME_ACCOUNTING
scripts/config -d LATENCYTOP
scripts/config -d PERF_EVENTS_AMD_POWER
scripts/config -d LOCK_TORTURE_TEST
scripts/config -d RCU_TORTURE_TEST
%endif

# NTFS3 is a kernel NTFS implementation, which offers much faster performance
# than the NTFS-3G FUSE based implementation. Note: ntfs3 requires the file
# system type to mount. e.g. mount -t ntfs3 /dev/sdxY /mnt
# https://www.paragon-software.com/home/ntfs3-driver-faq/
# https://wiki.archlinux.org/title/NTFS
scripts/config -m NTFS3_FS
scripts/config -d NTFS3_64BIT_CLUSTER
scripts/config -e NTFS3_LZX_XPRESS
scripts/config -e NTFS3_FS_POSIX_ACL

# Enable NTSYNC driver for fast kernel-backed Wine.
scripts/config -m NTSYNC

# Enable v4l2-loopback device.
# https://github.com/umlaeute/v4l2loopback
scripts/config -m V4L2_LOOPBACK

# The preemption behavior can be defined on boot preempt=none, voluntary,
# or full (default). Boot time param "rcutree.enable_rcu_lazy=1" can be
# used to switch RCU_LAZY on. 
scripts/config -e RCU_EXPERT
scripts/config -d PREEMPT_NONE
scripts/config -d PREEMPT_VOLUNTARY
scripts/config -e PREEMPT
scripts/config -e PREEMPT_DYNAMIC
scripts/config -e RCU_LAZY
scripts/config -e RCU_LAZY_DEFAULT_OFF
scripts/config --set-val RCU_FANOUT 32
scripts/config --set-val RCU_FANOUT_LEAF 16
scripts/config -e RCU_BOOST
scripts/config --set-val RCU_BOOST_DELAY 500
scripts/config -d RCU_CPU_STALL_CPUTIME
scripts/config -d RCU_EXP_KTHREAD
scripts/config -e RCU_NOCB_CPU
scripts/config -e RCU_NOCB_CPU_DEFAULT_ALL
scripts/config -d RCU_NOCB_CPU_CB_BOOST
scripts/config -d TASKS_TRACE_RCU_READ_MB
scripts/config -e RCU_DOUBLE_CHECK_CB_TIME
scripts/config -d RT_GROUP_SCHED
scripts/config -e SCHED_OMIT_FRAME_POINTER
scripts/config -d SCHED_CLUSTER

mv .config config

%build
BuildKernel() {

    Target=$1
    Arch=x86_64
    ExtraVer="-%{release}.${Target}"

    rm -f localversion*

    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = ${ExtraVer}/" Makefile

    make O=${Target} -s mrproper
    cp config ${Target}/.config
    make O=${Target} -s ARCH=${Arch} olddefconfig

    %if %{_localmodconfig} == 1
      # NVIDIA modules are built separately. Filter nvidia not found messages.
      yes "" | make O=${Target} -s ARCH=${Arch} localmodconfig 2>&1 | grep -v "^nvidia"

      # Add keyboard modules for the cpio package (do not remove).
      scripts/config --file ${Target}/.config -m SERIO_I8042
      scripts/config --file ${Target}/.config -m SERIO_LIBPS2
      scripts/config --file ${Target}/.config -m KEYBOARD_ATKBD
      scripts/config --file ${Target}/.config -m HID_LOGITECH_DJ
      scripts/config --file ${Target}/.config -m HID_LOGITECH_HIDPP
      scripts/config --file ${Target}/.config -m HID_APPLE

      # Add modules for File systems.
      scripts/config --file ${Target}/.config -m CUSE
      scripts/config --file ${Target}/.config -m VIRTIO_FS
      scripts/config --file ${Target}/.config -e FUSE_DAX
      scripts/config --file ${Target}/.config -m OVERLAY_FS
      scripts/config --file ${Target}/.config -d OVERLAY_FS_REDIRECT_DIR
      scripts/config --file ${Target}/.config -d OVERLAY_FS_REDIRECT_ALWAYS_FOLLOW
      scripts/config --file ${Target}/.config -d OVERLAY_FS_INDEX
      scripts/config --file ${Target}/.config -d OVERLAY_FS_XINO_AUTO
      scripts/config --file ${Target}/.config -d OVERLAY_FS_METACOPY
      scripts/config --file ${Target}/.config -d OVERLAY_FS_DEBUG

      # Add modules for Caches.
      scripts/config --file ${Target}/.config -m NETFS_SUPPORT
      scripts/config --file ${Target}/.config -d NETFS_STATS
      scripts/config --file ${Target}/.config -m CACHEFILES
      scripts/config --file ${Target}/.config -d CACHEFILES_DEBUG
      scripts/config --file ${Target}/.config -d CACHEFILES_ERROR_INJECTION
      scripts/config --file ${Target}/.config -d CACHEFILES_ONDEMAND

      # Add modules for CD-ROM/DVD and EXFAT/NTFS3 Filesystems.
      scripts/config --file ${Target}/.config -m ISO9660_FS
      scripts/config --file ${Target}/.config -e JOLIET
      scripts/config --file ${Target}/.config -e ZISOFS
      scripts/config --file ${Target}/.config -m UDF_FS
      scripts/config --file ${Target}/.config -m EXFAT_FS
      scripts/config --file ${Target}/.config --set-str EXFAT_DEFAULT_IOCHARSET "utf8"
      scripts/config --file ${Target}/.config -m NTFS3_FS
      scripts/config --file ${Target}/.config -d NTFS3_64BIT_CLUSTER
      scripts/config --file ${Target}/.config -e NTFS3_LZX_XPRESS
      scripts/config --file ${Target}/.config -e NTFS3_FS_POSIX_ACL

      # Add optional modules.
      scripts/config --file ${Target}/.config -m NTSYNC

    %endif

    yes "" | make O=${Target} -s ARCH=${Arch} \
      CONFIG_DEBUG_SECTION_MISMATCH=y %{?_smp_mflags} %{?sparse_mflags}
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
    cp %{buildroot}${ModDir}/kernel/drivers/input/serio/i8042.ko.zst      cpiofile${ModDir}/kernel/drivers/input/serio
    cp %{buildroot}${ModDir}/kernel/drivers/input/serio/libps2.ko.zst     cpiofile${ModDir}/kernel/drivers/input/serio
    cp %{buildroot}${ModDir}/kernel/drivers/input/keyboard/atkbd.ko.zst   cpiofile${ModDir}/kernel/drivers/input/keyboard
    cp %{buildroot}${ModDir}/kernel/drivers/hid/hid-logitech-dj.ko.zst    cpiofile${ModDir}/kernel/drivers/hid
    cp %{buildroot}${ModDir}/kernel/drivers/hid/hid-logitech-hidpp.ko.zst cpiofile${ModDir}/kernel/drivers/hid
    cp %{buildroot}${ModDir}/kernel/drivers/hid/hid-apple.ko.zst          cpiofile${ModDir}/kernel/drivers/hid
    cp %{buildroot}${ModDir}/modules.order   cpiofile${ModDir}
    cp %{buildroot}${ModDir}/modules.builtin cpiofile${ModDir}

    # Decompress the modules for the cpio file
    find cpiofile${ModDir} -name '*.ko.zst' -exec zstd -d --rm {} \;

    depmod -b cpiofile/usr ${Kversion}

    (
      cd cpiofile
      find . | cpio --create --format=newc \
        > ${KernelDir}/initrd-org.clearlinux.${Target}.%{version}-%{release}
    )
}

InstallKernel %{ktarget} %{kversion}

createCPIO %{ktarget} %{kversion}

rm -rf %{buildroot}/usr/lib/firmware

mkdir -p %{buildroot}/usr/share/package-licenses/linux-xmbore
cp COPYING %{buildroot}/usr/share/package-licenses/linux-xmbore/COPYING
cp -a LICENSES/* %{buildroot}/usr/share/package-licenses/linux-xmbore

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
/usr/share/package-licenses/linux-xmbore

%files cpio
/usr/lib/kernel/initrd-org.clearlinux.%{ktarget}.%{version}-%{release}

%files dev
%defattr(-,root,root)
/usr/lib/modules/%{kversion}/build
