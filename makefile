# Make wrapper for Amplify dev subnets
PYTHON = /usr/bin/python
ENVS = prod poc qa build patch

all:   
	for env in $(ENVS); do \
		$(MAKE) $$env; \
	done

base_vpc: base_vpc.py base-vpc.json
	$(PYTHON) base_vpc.py -c $(CONFIG)

vpc_with_update: vpc_with_update.py
	$(PYTHON) vpc_with_update.py -c $(CONFIG)

$(ENVS): vpc_with_update
	$(PYTHON) $@-env.py -c $(CONFIG)

