.PHONY: start
start:
	systemctl --user start warikanman.service
.PHONY: stop
stop:
	systemctl --user stop warikanman.service
.PHONY: restart
restart:
	systemctl --user restart warikanman.service
.PHONY: status
status:
	systemctl --user status warikanman.service
.PHONY: dreload
dreload:
	systemctl --user daemon-reload
.PHONY: access-db
access-db:
	mysql -u warikanman -pwarikanman warikanman

.PHONY: test
test:
	python -m unittest -v

.PHONY: deploy
deploy:
	cp /home/ubuntu/warikanman/deploy_config/nginx/default /etc/nginx/sites-available/default
	cp /home/ubuntu/warikanman/deploy_config/env/linebot_env.sh ~/linebot_env
	cp /home/ubuntu/warikanman/deploy_config/systemd/warikanman.service ~/.config/systemd/user/warikanman.service
	sudo cp -r /home/ubuntu/warikanman/deploy_config/html /var/www/

