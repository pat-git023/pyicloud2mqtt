docker:
	docker build -t pyicloud_mqtt:latest .

build:
	pip install -r requirements.txt
