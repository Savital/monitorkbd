obj-m	:= monitorkbd.o

KERNELDIR ?= /lib/modules/$(shell uname -r)/build
PWD       := $(shell pwd)

all:
	$(MAKE) -C $(KERNELDIR) M=$(PWD)
	rm -f *.o *~ core .depend .*.cmd *.mod.c .cache.mk
	rm -f Module.markers Module.symvers modules.order
	rm -rf .tmp_versions Modules.symvers

clean:
	rm -f *.o *~ core .depend .*.cmd *.ko *.mod.c
	rm -f Module.markers Module.symvers modules.order
	rm -rf .tmp_versions Modules.symvers

