.PHONY: build
build:
	docker build \
	-t nasza-warszawa \
	.

.PHONY: run_backend
run_backend:
	docker run \
	-d \
	-p 5000:5000 \
	-it nasza-warszawa