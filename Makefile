.PHONY: clean all

CC ?= clang
CFLAGS ?= -O2

LIBUSB_CFLAGS := $(shell pkg-config --cflags libusb-1.0)
LIBUSB_LIBS   := $(shell pkg-config --libs libusb-1.0)
# usbtool.c includes <libusb-1.0/libusb.h>; pkg-config points at .../libusb-1.0,
# so also add its parent (includedir) for that include form to resolve.
LIBUSB_INCDIR := $(shell pkg-config --variable=includedir libusb-1.0)

all:
	$(CC) $(CFLAGS) -I$(LIBUSB_INCDIR) $(LIBUSB_CFLAGS) usbtool.c -o usbtool $(LIBUSB_LIBS)

clean:
	rm -f usbtool
